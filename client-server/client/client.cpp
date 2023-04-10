#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdint.h>

#define BUF_SIZE 2048
#define FILE_SIZE 256
#define FILE_IS_NOT_EXIST 65535

using namespace std;

int main(int argc, char *argv[])
{
    int sockClient;
    int port, id;
    struct sockaddr_in serverAddr;
    char fileClient[FILE_SIZE];
    char fileServer[FILE_SIZE];
    uint8_t sendBuf[BUF_SIZE];
    uint8_t recvBuf[BUF_SIZE];
    int  nbytes;
    int  sizeData;
    ofstream responseFile;

    srand(time(NULL));

    if (argc != 3)
    {
        fprintf(stderr, "Error: incorrect number of arguments\n");
        fprintf(stderr, "Usage: ./client port id\n");
        return 1;
    }

    if ((sockClient = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket");
        return 1;
    }

    port = atoi(argv[1]);
    id = atoi(argv[2]);

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    serverAddr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    if (connect(sockClient, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1)
    {
        perror("connect"); 
        return 1;
    }

    system("mkdir responses -p");

    sprintf(fileServer, "file%d", rand() % 10);
    // sprintf(fileServer, "image.jpg");
    strcpy(fileClient, "responses/");
    strncat(fileClient, fileServer, strlen(fileServer));
    sprintf(fileClient + strlen("responses/") + strlen(fileServer), "_client%d", id);
    
    strcpy((char*)sendBuf, fileServer);

    if ((nbytes = write(sockClient, sendBuf, strlen(fileServer))) == -1)
    {
        perror("write");
        return 1;
    }

    while ((nbytes = read(sockClient, recvBuf, sizeof(recvBuf))) > 0)
    {
        sizeData = (recvBuf[1] << 8) + recvBuf[0];

        if(sizeData == FILE_IS_NOT_EXIST)
        {
            printf("Requested file \"%s\" isn't exist\n", fileServer);
            break;
        }
        else
        {
            if(!responseFile.is_open())
                responseFile.open(fileClient);
            
            responseFile.write((const char*)&recvBuf[2], sizeData);
        }
    }

    close(sockClient);
    responseFile.close();
}