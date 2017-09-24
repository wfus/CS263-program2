#include "stdio.h"
#include "stdint.h"



char* load_file(char const* path)
{
    char* buffer = 0;
    long length;
    FILE * f = fopen (path, "rb"); //was "rb"

    if (f)
    {
      fseek (f, 0, SEEK_END);
      length = ftell (f);
      fseek (f, 0, SEEK_SET);
      buffer = (char*)malloc ((length+1)*sizeof(char));
      if (buffer)
      {
        fread (buffer, sizeof(char), length, f);
      }
      fclose (f);
    }
    buffer[length] = '\0';
    // for (int i = 0; i < length; i++) {
    //     printf("buffer[%d] == %c\n", i, buffer[i]);
    // }
    //printf("buffer = %s\n", buffer);

    return buffer;
}

int main()
{
	uint8_t* dbinput = malloc(100000);
	uint8_t* output = malloc(100000);
	uint8_t* key = malloc(16);

	*key = "\x3b\x99\xc2\x16\xf1\xae\x2d\xd6\x9b\x70\xf5\xe8\x00\xfc\x9a\xec";	
	dbinput = load_file("/home/httpd/reverse-engineering/leaked_app/password.db");

	printf(dbinput);
	printf(key);

	return 0;
}

