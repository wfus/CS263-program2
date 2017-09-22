/**
 * crackpw.c
 *
 * TODO: briefly describe how this cracker works.
 */

#include "hashpw.h"  // so that you can call hashpw()


/**
 * Given a hash, tries to generate a cleartext ASCII password that hashes to
 * the same value.
 *
 * If successful, returns the length of the cracked password and stores the
 * cracked password in "dest". If unsuccessful, returns 0.
 */
int crackpw(char dest[256], unsigned int hash) {
    // TODO: implement this. Don't forget to null-terminate dest!
    return 0;
}
