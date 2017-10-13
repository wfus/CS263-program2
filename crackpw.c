/**
 * crackpw.c
 *
 * TODO: briefly describe how this cracker works.
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
        /* note that fgets don't strip the terminating \n, checking its
           presence would allow to handle lines longer that sizeof(line) */
        // printf("%s", line);
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
