#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h> 
#include <ctype.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/shm.h> 
#include <sys/mman.h>
#include <semaphore.h>

#define SHM "shm"
#define SEM "sem"
#define SHM_SIZE 1024
#define BUFSIZE 50

typedef struct{
    char proc;
    char data[BUFSIZE];
    int exit;
} SharedData;

double calculate(const char* expr)
{
    char operand1[10];
    char operand2[10];
    int index_operator;
    int i, j;

    for(i = 0; isdigit(expr[i]); ++i)
        operand1[i] = expr[i];
    
    index_operator = i++;

    for(j = 0; isdigit(expr[i]); ++i, ++j)
        operand2[j] = expr[i];

    switch (expr[index_operator])
    {
    case '+':
        return atoi(operand1) + atoi(operand2);
    case '-':
        return atoi(operand1) - atoi(operand2);
    case '*':
        return atoi(operand1) * atoi(operand2);
    case '/':
        return (double)atoi(operand1) / atoi(operand2);    
    }
}

int main()
{
    char expr[BUFSIZE];
    char result[BUFSIZE];
    int shm_fd = shm_open(SHM, O_CREAT | O_RDWR, 0666); 
    void *ptr = mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0); 

    sem_t *semptr = sem_open(SEM, O_CREAT, 0666, 0);
    if(semptr == SEM_FAILED)
    {
        fprintf(stderr, "Error: sem_open()");
        return 1;
    }

    while(!sem_wait(semptr))
    {
        if(((SharedData*)ptr)->exit) 
        {
            sem_post(semptr);
            break;
        }
        if(((SharedData*)ptr)->proc == 'B')
        {
            sprintf(((SharedData*)ptr)->data, "%s=%f", ((SharedData*)ptr)->data, calculate(((SharedData*)ptr)->data));
            printf("C: expr_result = %s\n", ((SharedData*)ptr)->data);
            ((SharedData*)ptr)->proc = 'C';
        }
        sem_post(semptr);
    }

    sem_close(semptr);
    printf("End C\n");
    return 0;
}