#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h> 
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/shm.h> 
#include <sys/mman.h>
#include <semaphore.h>

#define FIFO "fifo"
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
    mkfifo(FIFO, 0666);
    char expr[BUFSIZE];
    int shm_fd = shm_open(SHM, O_CREAT | O_RDWR, 0666); 
    ftruncate(shm_fd, SHM_SIZE); 
    void *ptr = mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

    sem_t *semptr = sem_open(SEM, O_CREAT, 0666, 0);
    if(semptr == SEM_FAILED)
    {
        fprintf(stderr, "B Error: sem_open()");
        return 1;
    }

    SharedData shd;
    shd.proc = 'D';
    shd.exit = 0;
    memcpy(ptr, (SharedData*)&shd, sizeof(shd));

    int fd = open(FIFO, O_RDONLY);

    do
    {
        if(((SharedData*)ptr)->proc == 'D')
        {
            read(fd, ((SharedData*)ptr)->data, BUFSIZE);
            if(!strlen(((SharedData*)ptr)->data))
            {
                ((SharedData*)ptr)->exit = 1;
                sem_post(semptr);
                break;
            }
            printf("B: expr = %s\n", ((SharedData*)ptr)->data);
            ((SharedData*)ptr)->proc = 'B';
        }
        sem_post(semptr);
    } while(!sem_wait(semptr));

    close(fd);
    sem_close(semptr);
    printf("End B\n");
    return 0;
}