#!/usr/bin/env python3

# Do NOT change this file! In fact, it might be inadvisable even to read this
# file, since much has been obfuscated to prevent reverse-engineering of the
# solution. The test case error messages should be enough to debug your
# solution.

from binascii import hexlify as tohex
import csv
import hashlib
import os
import pathlib
import shlex
import string
import subprocess

from nose.tools import with_setup


TEST_DIR = pathlib.Path(__file__).parent
ROOT_DIR = TEST_DIR.parent
APP_DIR = ROOT_DIR / 'leaked_app'


def _run(cmd,
         stdin=subprocess.DEVNULL,
         stderr=subprocess.DEVNULL,
         timeout=None):
    try:
        exec_result = subprocess.check_output(
            cmd,
            stdin=stdin,
            stderr=stderr,
            timeout=timeout,
        )
    except subprocess.CalledProcessError:
        assert False, \
            "`{}` finished with non-zero exit code.".format(
                ' '.join(map(shlex.quote, cmd)))
    except subprocess.TimeoutExpired:
        assert False, \
            "`{}` timed out (exceeded {:.1f}s).".format(
                ' '.join(map(shlex.quote, cmd)), timeout)

    lastline = exec_result.splitlines()[-1]
    return lastline.strip().lower()


def _iter_hash(b, iters=10000):
    for _ in range(iters):
        b = hashlib.sha512(b).digest()
    return b


def test_keys():
    needles = [
        b'28f7b6ba10dbe3389ebf299bcbb0b289123a60aab853fa6c50fc1e87f6245e16a88de70f84c8b9d7fb0cd4f6facadc693f2990175329917f8d6066cb14699100',
        b'87bf74053a820258a3a1f5cc8976192773abd0e391201c5d055d0c4f2d1912d0b516aa1994811fef7ccc831f4694243a63a1710533fd0d504e20cbc838c23ab8',
        b'd90fabcbfe2f9cf7d4c280c13ec5412206289f20b7cbabe840ab8a03cce1bab07fa813c6a1a7608085c2a71b58d79dce7aae420e1d1f9bfcc8b2c5a2de8ed0ac',
    ]
    expected_summary = b'c96fde34472bc4fdda6ef224f6b57d8ec2d1d5e86868b616e2ca1771f726b969b92e133ccdf7c5b877047bf53c0af74fd3c9f0e0321c3fd18a43509464bdc042'

    summary = b''
    with open(str(ROOT_DIR / 'keys.txt'), 'r') as infile:
        toks = ''.join((c if c in string.hexdigits else ' ')
                       for c in infile.read()).split()
        for tok in toks:
            tok = tok.lower().encode()
            if tok.startswith(b'0x'):  # Get rid of leading 0x
                tok = tok[2:]

            tok_hash = tohex(_iter_hash(tok))
            if tok_hash in needles:
                needles.remove(tok_hash)
                summary += tok + tok_hash

    assert tohex(_iter_hash(summary)) == expected_summary, \
        'The correct encryption key(s) were not found in keys.txt ' + \
        '(make sure it is a hex string!).'


def test_hasher():
    with open(str(TEST_DIR / 'hr.csv'), 'r') as infile:
        reader = csv.reader(infile)
        cases = list(reader)

    for plaintext, hashed_hash in cases:
        cmd = ['./hasher', plaintext]
        assert (tohex(_iter_hash(_run(cmd, timeout=0.1))) ==
                hashed_hash.encode()), \
            "Your hash function is incorrect for plaintext '{}'".format(
                plaintext)


def _get_master():
    ret = {}
    with open(str(TEST_DIR / 't.csv'), 'r') as infile:
        for u, h in csv.reader(infile):
            ret[u] = h

    return ret


def _test_plaintext(filename, num_needed, require_root=True):
    master = _get_master()

    with open(str(ROOT_DIR / filename), 'r') as infile:
        answer = list(csv.DictReader(infile))
    assert len(answer) >= num_needed, \
        '{} needs at least {} username/password pairs.'.format(
            filename, num_needed)

    assert len(set(entry['username'] for entry in answer)) == len(answer), \
        'Usernames in {} are not unique.'.format(filename)

    if require_root:
        root_idx = next((i for i, entry in enumerate(answer)
                         if entry['username'] == 'root'), -1)

        assert root_idx > -1, \
            '{} needs to have the root user/pass.'.format(filename)

        tmp = answer[0]
        answer[0] = answer[root_idx]
        answer[root_idx] = tmp

    answer = answer[:num_needed]

    for entry in answer:
        username, password = entry['username'].strip(), entry['password'].strip()
        entry['username'], entry['password'] = username, password
        assert username in master, \
            'User {} does not exist in the database.'.format(username)
        hashed = _run(['./hasher', password], timeout=0.1)
        hashed_hash = tohex(_iter_hash(username.encode() + hashed))
        assert hashed_hash == master[username].encode(), \
            "'{}' is an incorrect password for user {}".format(
                password, username)

    return answer


def test_cracker():
    num_needed = 8
    timeout_secs = 120

    answer = _test_plaintext('plaintext-passwords-cracker.csv', num_needed)
    for entry in answer:
        username, password = entry['username'], entry['password']
        hashed = _run(['./hasher', password], timeout=0.1)
        cmd = ['./cracker', hashed.decode()]

        cracked = _run(cmd, timeout=timeout_secs)
        hash_cracked = _run(['./hasher', cracked], timeout=0.1)
        assert hash_cracked == hashed, \
            "Incorrect: your cracker gave '{}' for the hash {}.".format(
                cracked.decode(), hashed)


def test_network_cracker():
    num_needed = 4
    timeout_secs = 120
    proton_port = 22263

    answer = _test_plaintext('plaintext-passwords-network-cracker.csv',
                             num_needed)
    os.environ['LD_LIBRARY_PATH'] = str(APP_DIR)
    with subprocess.Popen(['./proton', str(proton_port), '.'],
                          cwd=str(APP_DIR),
                          stdin=subprocess.DEVNULL,
                         ) as proton_proc:
        try:
            for entry in answer:
                username, password = entry['username'], entry['password']
                hashed = _run(['./hasher', password], timeout=0.1)
                cmd = ['./network_cracker.sh', username,
                       'localhost', str(proton_port)]

                cracked = _run(cmd, timeout=timeout_secs)
                hash_cracked = _run(['./hasher', cracked], timeout=0.1)
                assert hash_cracked == hashed, \
                    "Incorrect: your cracker gave '{}' for user '{}'.".format(
                        cracked.decode(), username)

        finally:
            subprocess.call(['pkill', '-f', 'proton.*' + str(proton_port)])
