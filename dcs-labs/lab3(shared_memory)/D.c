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

int main()
{
    int shm_fd = shm_open(SHM, O_CREAT | O_RDWR, 0666); 
    void *ptr = mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0); 

    sem_t *semptr = sem_open(SEM, O_CREAT, 0666, 0);
    if(semptr == SEM_FAILED)
    {
        fprintf(stderr, "D Error: sem_open()");
        return 1;
    }

    FILE *file = fopen("results", "w");

    while(!sem_wait(semptr))
    {
        if(((SharedData*)ptr)->exit) 
        {
            sem_post(semptr);
            break;
        }
        if(((SharedData*)ptr)->proc == 'C')
        {
            fputs(((SharedData*)ptr)->data, file);
            fputc('\n', file);
            printf("D: write data in file\n");
            ((SharedData*)ptr)->proc = 'D';
        }
        sem_post(semptr);
    }

    fclose(file);
    sem_close(semptr);
    sem_unlink(SEM);
    shm_unlink(SHM);
    printf("End D\n");
    return 0;
}