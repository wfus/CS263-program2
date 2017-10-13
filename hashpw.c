/**
 * hashpw.c
 *
 * TODO: thoroughly describe how you reverse-engineered the hash function.
 */


unsigned int hashpw(const char* plaintext, int len) {
	
	unsigned int pt = 0;
	unsigned int hash = 0;
	int ctr = 0;
	
	while (ctr < len) {
		pt = (ctr + plaintext)[0];
		hash = hash ^ ((pt << 8) + pt);
		hash = hash << 1;
		ctr++;
	}

	if (len > 0) {
		hash = hash | plaintext[0];
	} 

	hash = hash ^ 0xfeedface;
	return hash;
}
