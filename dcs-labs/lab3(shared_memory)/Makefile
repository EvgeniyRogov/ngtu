CC = gcc
PROG_A = A
PROG_B = B
PROG_C = C
PROG_D = D

$(PROG_A) : A.c
	$(CC) $^ -o $@ -g

$(PROG_B) : B.c
	$(CC) $^ -o $@ -g -lrt -lpthread

$(PROG_C) : C.c
	$(CC) $^ -o $@ -g -lrt -lpthread

$(PROG_D) : D.c
	$(CC) $^ -o $@ -g -lrt -lpthread
