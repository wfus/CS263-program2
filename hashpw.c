/**
 * hashpw.c
 * -----------------------
 * I mostly just looked at the assembly, allocating variables and 
 * tracking the registers by hand. For a thorough description, the 
 * comments that I made for myself while going through the assembly
 * are pasted as a comment below: 
 */

/**
08048c1b <calculate_pw_hash>:
push   %ebp
mov    %esp,%ebp
sub    $0x10,%esp
movl   $0x0,-0xc(%ebp)      // Initialize 4 byte variable A
movl   $0x0,-0x8(%ebp)      // Initialize 4 byte variable B, C
jmp    8048c59 <calculate_pw_hash+0x3e>

// B is used as a counter, looping through the plaintext string
mov    -0x8(%ebp),%edx     // move B to %edx
mov    0x8(%ebp),%eax      // move 1st parameter to eax
add    %edx,%eax           // add B and 2nd parameter
movzbl (%eax),%eax         // MOVZBL and MOVSBL is equivalent to 
movsbl %al,%eax            // getting an index [i] from an array
mov    %eax,-0x4(%ebp)     // put that value in C
mov    -0x4(%ebp),%eax.    // put C in eax  
shl    $0x8,%eax           // bitshift C by 8
mov    %eax,%edx.          // put (C << 8) in edx
mov    -0x4(%ebp),%eax.    // put C in eax
add    %edx,%eax.          // put (C << 8) + c) in eax
xor    %eax,-0xc(%ebp).    // A ^= (C << 8) + C 
shll   -0xc(%ebp).         // bitshift A by 1 (A << 1)
addl   $0x1,-0x8(%ebp).    // increment B
mov    -0x8(%ebp),%eax
cmp    0xc(%ebp),%eax.     // if second parameter is less than B
jl     8048c31 <calculate_pw_hash+0x16>
cmpl   $0x0,0xc(%ebp).     // jump if 2nd parameter is 0
jle    8048c73 <calculate_pw_hash+0x58>

mov    0x8(%ebp),%eax
movzbl (%eax),%eax
movsbl %al,%eax
or     %eax,-0xc(%ebp)
mov    -0xc(%ebp),%eax.   
xor    $0xfeedface,%eax   // xor A with 0xFEEDFACE
mov    %eax,-0xc(%ebp)    // put A in the return place  
mov    -0xc(%ebp),%eax

leave
ret
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
