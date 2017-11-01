#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <dlfcn.h>

#define MAXBUFLEN 1000000


void load_file(char* input, const char* filepath) {
	FILE *fp = fopen(filepath, "rb");
	if (fp != NULL) {
		size_t newLen = fread(input, sizeof(char), MAXBUFLEN, fp);
		if (newLen == 0) {
			fputs("Error reading file", stderr);
		} else {
			input[++newLen] = '\0'; /* Just to be safe. */
		}

		fclose(fp);
	}
}



int main()
{
	uint8_t* dbinput = malloc(100000);
	uint8_t* output = malloc(100000);
	uint8_t* key = malloc(16);

	key = "\x3b\x99\xc2\x16\xf1\xae\x2d\xd6\x9b\x70\xf5\xe8\x00\xfc\x9a\xec";	
	load_file(dbinput, "/home/httpd/reverse-engineering/leaked_app/password.db");

	printf("%s", dbinput);
	printf("\n\n");
	printf("%s", key);
	printf("\n\n");


	void* handle;
	void (*decrypt)(uint8_t*, uint8_t*, uint8_t*);
	char* error;

	handle = dlopen ("/home/httpd/reverse-engineering/leaked_app/libaes.so.1", RTLD_LAZY);
	error = dlerror ();
	if (error) {
		printf ("%s\n", error);
		exit (1);
	}

	decrypt = dlsym(handle, "AES128_ECB_decrypt");
	decrypt(dbinput, key, output);

	printf("%s", output);
	printf("\n\n");







	//free(dbinput);
	//free(output);
	//free(key);

	return 0;
}

