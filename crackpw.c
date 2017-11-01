/**
 * crackpw.c
 * -----------------
 * This cracker basically just gets a list of commonly used passwords, in 
 * this case RockYouTop25000, and then hashes each of the passwords on that
 * list. If the hash matches with the hashed password in the database, we
 * have a match and we can return. If we go through all possibilities and
 * don't find a match, we return 0 for unsuccessful search.
 */

#include "hashpw.h"  // so that you can call hashpw()
#include <stdio.h>
#include <string.h>

/**
 * Given a hash, tries to generate a cleartext ASCII password that hashes to
 * the same value.
 *
 * If successful, returns the length of the cracked password and stores the
 * cracked password in "dest". If unsuccessful, returns 0.
 */
int crackpw(char dest[256], unsigned int hash) {
    // Don't forget to null-terminate dest!
        


    const char* fileName = "data/rockyoupasswords.txt"; 
    FILE* file = fopen(fileName, "r"); /* should check the result */
    char line[256];

    while (fgets(line, sizeof(line), file)) {
	int length = strlen(line) - 1;
        if (hashpw(line, length) == hash) {
		strncpy(dest, line, length);
                dest[length] = '\0';
		return length;
	}	 
    }
    fclose(file);
    return 0;
}
