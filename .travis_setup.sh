#!/usr/bin/env bash

# Do NOT change this file!


set -e
cd leaked_app/
ln -sf libaes.so.1.0 libaes.so.1
ln -sf libaes.so.1.0 libaes.so
ln -sf libpassdb.so.1.0 libpassdb.so.1
ln -sf libpassdb.so.1.0 libpassdb.so
ls -l
