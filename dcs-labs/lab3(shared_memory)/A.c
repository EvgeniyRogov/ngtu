#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h> 
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <signal.h>

#define BUFSIZE 50
#define SEC 3
#define FIFO "fifo"

int sigStatus = 0;

void signalHandle()
{
    sigStatus = 1;
}

int main()
{
    char expr[BUFSIZE];
    char operators[4] = {'+', '-', '*', '/'};

    signal(SIGINT, signalHandle);
    mkfifo(FIFO, 0666);
    srand(time(NULL));
    int fd = open(FIFO, O_WRONLY);

    while(!sigStatus)
    {
        sprintf(expr, "%d%c%d", rand() % 100, operators[rand() % 4], rand() % 100 + 1);
        write(fd, expr, strlen(expr) + 1);
        printf("A: expr = %s\n", expr);
        sleep(rand() % SEC + 1);
    }

    write(fd, "\0", 1);

    close(fd);
    printf("End A\n");

    return 0;
}