#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <sys/types.h>
#include <unistd.h>
#include <poll.h>
#include <signal.h>

#define LIMIT_SEC 10
#define BUFSIZE 50

void createFileTasks(const char* filename, int numOfTasks)
{
    FILE *file = fopen(filename, "w");

    if(!file)
    {
        fprintf(stderr, "Error: can't open file");
        exit(EXIT_FAILURE);
    }

    srand(time(NULL));

    char task_str[BUFSIZE];

    for(int i = 0; i < numOfTasks; ++i)
    {
        sprintf(task_str, "task%d %d\n", i + 1, rand() % LIMIT_SEC + 1);
        fputs(task_str, file);
    }

    fclose(file);     
}

int getSeconds(const char* task)
{
    int i = 0;
    int j = 0;
    char secStr[10];
    while(task[i] != ' ') ++i;
    while(task[i] == ' ') ++i;
    while(task[i])
    {
        secStr[j++] = task[i];
        ++i;
    }
    return atoi(secStr);
}

int getNumTask(const char* task)
{
    char strNumTask[10];
    int j = 0;
    for(int i = 0; task[i] != ' '; ++i)
        if(isdigit(task[i]))
            strNumTask[j++] = task[i];
    return atoi(strNumTask);
}

static int sigStatus = 0;

void signalHandle()
{
    sigStatus = 1;
}

int main(int argc, char* argv[])
{
    /* pattern: ./lab2 -p 5 -t 30 -f filename */
    if(argc != 7)
    {
        fprintf(stderr, "argc error\n");
        return 1;
    }

    int numOfProcess;
    int numOfTasks;
    char filename[BUFSIZE];

    for (int i = 1; i < argc - 1; ++i)
    {
        if(!strcmp(argv[i], "-p"))
            numOfProcess = atoi(argv[i + 1]);
        if(!strcmp(argv[i], "-f"))
            strcpy(filename, argv[i + 1]);
        if(!strcmp(argv[i], "-t"))
            numOfTasks = atoi(argv[i + 1]);
    }

    createFileTasks(filename, numOfTasks);

    pid_t pids[numOfProcess];
    int pipes1[numOfProcess][2]; /* parent writes, child reads */
    int pipes2[numOfProcess][2]; /* parent reads, child writes */

    for(int p = 0; p < numOfProcess; ++p)
    {
        if(pipe(pipes1[p]) < 0)
        {
            fprintf(stderr, "Error: pipe()");
            return 1;
        }

        if(pipe(pipes2[p]) < 0)
        {
            fprintf(stderr, "Error: pipe()");
            return 1;
        }

        pids[p] = fork();

        if(pids[p] < 0)
        {
            fprintf(stderr, "Error: fork()\n");
            return 1;
        }
        else if(pids[p] == 0)
        {
            /* child process */
            signal(SIGUSR1, signalHandle);
            close(pipes1[p][1]);
            close(pipes2[p][0]);
            char readTask[BUFSIZE];
            char writeResponse[BUFSIZE];
            writeResponse[0] = '\0';
            for(;;)
            {
                write(pipes2[p][1], writeResponse, strlen(writeResponse) + 1);
                read(pipes1[p][0], readTask, BUFSIZE);
                if(sigStatus) break;
                sprintf(writeResponse, "pid = %d, n_task = %d\n", getpid(), getNumTask(readTask));
                sleep(getSeconds(readTask));
            }
            close(pipes1[p][0]);
            close(pipes2[p][1]);
            return 0;
        }
    }

    struct pollfd fds[numOfProcess];

    for(int p = 0; p < numOfProcess; ++p)
    {
        close(pipes1[p][0]);
        close(pipes2[p][1]);
        fds[p].fd = pipes2[p][0];
        fds[p].events = POLLIN;
        fds[p].revents = 0;
    }

    FILE *file = fopen(filename, "r");
    FILE *reportFile = fopen("report", "w");
    char task[BUFSIZE];
    char reportBuf[BUFSIZE];

    for(;;)
    {
        if(poll(fds, numOfProcess, LIMIT_SEC * 1000) <= 0) break;
        for (int p = 0; p < numOfProcess; ++p)
        {
            if(fds[p].revents & POLLIN) 
            {
                fds[p].revents = 0;
                read(fds[p].fd, reportBuf, BUFSIZE);
                if(strlen(reportBuf) != 0)
                    fputs(reportBuf, reportFile);
                if(fgets(task, BUFSIZE, file) != NULL)
                {
                    write(pipes1[p][1], task, strlen(task) + 1);
                    printf("send task%d\n", getNumTask(task));
                }
            }
        }
    }

    for(int p = 0; p < numOfProcess; ++p)
    {
        close(pipes1[p][1]);
        close(pipes2[p][0]);
        kill(pids[p], SIGUSR1);
    }

    fclose(file);
    fclose(reportFile);

    return 0;
}