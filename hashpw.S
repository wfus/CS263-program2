	.file	"hashpw.c"
	.text
	.globl	hashpw
	.type	hashpw, @function
hashpw:
.LFB0:
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$16, %esp
	movl	$0, -4(%ebp)
	movl	$0, -12(%ebp)
	movl	$0, -8(%ebp)
	jmp	.L2
.L3:
	movl	-8(%ebp), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movzbl	(%eax), %eax
	movsbl	%al, %eax
	movl	%eax, -4(%ebp)
	movl	-4(%ebp), %eax
	sall	$8, %eax
	movl	%eax, %edx
	movl	-4(%ebp), %eax
	addl	%edx, %eax
	xorl	%eax, -12(%ebp)
	sall	-12(%ebp)
	addl	$1, -8(%ebp)
.L2:
	movl	-8(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	.L3
	cmpl	$0, 12(%ebp)
	jns	.L4
	movl	8(%ebp), %eax
	movzbl	(%eax), %eax
	movsbl	%al, %eax
	orl	%eax, -12(%ebp)
.L4:
	xorl	$-17958194, -12(%ebp)
	movl	-12(%ebp), %eax
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE0:
	.size	hashpw, .-hashpw
	.ident	"GCC: (Ubuntu 4.8.4-2ubuntu1~14.04.3) 4.8.4"
	.section	.note.GNU-stack,"",@progbits
