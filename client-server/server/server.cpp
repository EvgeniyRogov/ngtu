#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdint.h>
#include <signal.h>
#include <queue>

#define BUF_SIZE 2048
#define FILE_SIZE 256
#define NUM_OF_THREADS 3

using namespace std;

queue <int> clients;
pthread_mutex_t mutex;
pthread_cond_t cond;

int generateFiles(const char* dirname, const int nFiles, const int maxLines);
void* handleClient(void* args);
void* handleAccept(void* args);
void transferFile(int sockClient);
void signalHandler(int sig);

int main(int argc, char* argv[])
{
    int sockListener;
    int sockClient;
    int port;
    struct sockaddr_in addr;
    pthread_t threadsHandleClient[NUM_OF_THREADS];
    pthread_t threadHandleAccept;
    struct sigaction s;

    if (argc != 2)
    {
        fprintf(stderr, "Error: incorrect number of arguments\n");
        fprintf(stderr, "Usage: ./server port");
        return 1;
    }

    if (generateFiles("storage", 10, 1000000))
        return 1;
    
    if ((sockListener = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket"); 
        return 1;
    }

    port = atoi(argv[1]);

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sockListener, (struct sockaddr*)&addr, sizeof(addr)) == -1)
    {
        perror("bind");
        return 1;
    }

    if (listen(sockListener, 5) == -1)
    {
        perror("listen"); 
        return 1;
    }

    pthread_mutex_init(&mutex, NULL);

    if (pthread_create(&threadHandleAccept, NULL, handleAccept, (void*)&sockListener) != 0)
    {
        perror("pthread_create"); 
        return 1;
    }

    for (int i = 0; i < NUM_OF_THREADS; ++i)
    {
        if (pthread_create(&threadsHandleClient[i], NULL, handleClient, NULL) != 0)
        {
            perror("pthread_create"); 
            return 1;
        }
    }

    printf("Listening port %d ...\n", port);

    s.sa_handler = signalHandler;
    sigemptyset(&s.sa_mask);
    s.sa_flags = 0;
    sigaction(SIGINT, &s, NULL);

    pause();

    pthread_mutex_destroy(&mutex);
    printf("Server is stopped\n");

    return 0;
}


int generateFiles(const char* dirname, const int nFiles, const int maxLines)
{
    char filename[FILE_SIZE];
    srand(time(NULL));

    if (mkdir(dirname, 0777) == -1)
    {
        if (errno != 17)
        {
            perror("mkdir");
            return 1;
        }
    }

    for (int i = 0; i < nFiles; ++i)
    {
        sprintf(filename, "%s/file%d", dirname, i);
        ofstream file(filename);
        int iters = rand() % maxLines;
        for (int i = 0; i < iters; ++i)
            file << "Hello from " << filename << endl;
        file.close();
    }
    
    return 0;
}

void* handleClient(void* args)
{
    int sockClient;

    for (;;)
    {
        pthread_mutex_lock(&mutex); 
        while (clients.empty())
        {
            printf("thread %d\n", pthread_self());
            pthread_cond_wait(&cond, &mutex);
        }
        sockClient = clients.front();
        clients.pop();
        pthread_mutex_unlock(&mutex);
        transferFile(sockClient);
    }
}

void transferFile(int sockClient)
{
    char fileServer[FILE_SIZE];
    uint8_t sendBuf[BUF_SIZE];
    uint8_t recvBuf[BUF_SIZE];
    int  curSizeData;
    int  nbytes;

    if ((nbytes = read(sockClient, recvBuf, sizeof(recvBuf))) == -1)
    {
        perror("read");
        exit(1);
    }

    strcpy(fileServer, "storage/");
    strncat(fileServer, (const char *)recvBuf, nbytes);

    ifstream file(fileServer);

    file.seekg(0, file.end);
    nbytes = file.tellg();
    file.seekg(0, file.beg);

    for (;;)
    {
        if (nbytes > BUF_SIZE)
            curSizeData = BUF_SIZE - 2;
        else
            curSizeData = nbytes;

        memcpy(sendBuf, &curSizeData, 2);
        file.read((char*)&sendBuf[2], curSizeData);
        file.seekg(0, ios::cur);
        nbytes -= curSizeData;
        write(sockClient, sendBuf, sizeof(sendBuf));

        if (nbytes <= 0) break;
    }

    file.close();
    close(sockClient);
}

void* handleAccept(void* args)
{
    int sockClient;
    int sockListener = *((int*)args);

    for (;;)
    {
        if ((sockClient = accept(sockListener, NULL, NULL)) == -1)
        {
            perror("accept");
            exit(1);
        }
        printf("Connection accepted, socket = %d\n", sockClient);

        pthread_mutex_lock(&mutex);
        clients.push(sockClient);
        pthread_mutex_unlock(&mutex);
        pthread_cond_broadcast(&cond);
    }
}

void signalHandler(int sig) {}