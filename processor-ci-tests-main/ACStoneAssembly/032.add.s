	.file	"032.add.c"
	.option nopic
	.attribute arch, "rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.align	2
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sw	s0,28(sp)
	addi	s0,sp,32
	li	a5,255
	sh	a5,-18(s0)
	li	a5,-256
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,-20
	sh	a5,-18(s0)
	li	a5,-30
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,-2
	sh	a5,-18(s0)
	li	a5,2
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,10
	sh	a5,-18(s0)
	li	a5,-5
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,5
	sh	a5,-18(s0)
	li	a5,-10
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,4096
	addi	a5,a5,-241
	sh	a5,-18(s0)
	li	a5,-4096
	addi	a5,a5,240
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	li	a5,-20480
	addi	a5,a5,-1366
	sh	a5,-18(s0)
	li	a5,20480
	addi	a5,a5,1365
	sh	a5,-20(s0)
	lhu	a4,-18(s0)
	lhu	a5,-20(s0)
	add	a5,a4,a5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-22(s0)
	sh	zero,-22(s0)
	sh	zero,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,1
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,2
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,3
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,4
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	sh	zero,-24(s0)
	li	a5,255
	sh	a5,-26(s0)
	li	a5,-256
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,-20
	sh	a5,-26(s0)
	li	a5,-30
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,-2
	sh	a5,-26(s0)
	li	a5,2
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,10
	sh	a5,-26(s0)
	li	a5,-5
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,5
	sh	a5,-26(s0)
	li	a5,-10
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,4096
	addi	a5,a5,-241
	sh	a5,-26(s0)
	li	a5,-4096
	addi	a5,a5,240
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	li	a5,-20480
	addi	a5,a5,-1366
	sh	a5,-26(s0)
	li	a5,20480
	addi	a5,a5,1365
	sh	a5,-28(s0)
	lhu	a5,-26(s0)
	mv	a4,a5
	lhu	a5,-28(s0)
	add	a5,a4,a5
	sh	a5,-30(s0)
	sh	zero,-30(s0)
	sh	zero,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,1
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,2
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,3
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,4
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,5
	sh	a5,-32(s0)
	sh	zero,-32(s0)
	li	a5,15
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,-1
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,-2
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,-3
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,-4
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	lhu	a5,-24(s0)
	addi	a5,a5,-5
	slli	a5,a5,16
	srli	a5,a5,16
	sh	a5,-24(s0)
	sh	zero,-24(s0)
	li	a5,15
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,-1
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,-2
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,-3
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,-4
	sh	a5,-32(s0)
	lhu	a5,-32(s0)
	addi	a5,a5,-5
	sh	a5,-32(s0)
	sh	zero,-32(s0)
	li	a5,0
	mv	a0,a5
	lw	s0,28(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC: () 13.2.0"
