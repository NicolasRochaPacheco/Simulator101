# File asm/test.asm "Test Program"
# Loads two numbers and adds them


.global	_main

_main:
	addi x1, x0, 3
	addi x2, x0, 2
	add  x3, x1, x2
