#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

#include "generator.h"
#include "XmlParser/xmlparser.h"

#define PATH_PROG "wordcounter"

typedef struct 
{
	int numberOfProcess;
	char inputPrefix[256];
	char outputPrefix[256];
	int maxFileSize;
} Input;

void clearDirectory(char *pathDir);

int main(int argc, char *argv[])
{
    XmlNode* rootNode = createXmlTree("config.xml");
    if(!rootNode)
    {
        fprintf(stderr, "Error: createXmlTree()\n");
        return 1;
    }

    Input input;
    char content[1000];
    content[0] = '\0';

    getContent(rootNode, "NumberOfProcess", content);
    input.numberOfProcess = atoi(content);
    getContent(rootNode, "InputPrefix", content);
    strcpy(input.inputPrefix, content);
    getContent(rootNode, "OutputPrefix", content);
    strcpy(input.outputPrefix, content);
    getContent(rootNode, "MaxFileSize", content);
    input.maxFileSize = atoi(content);

    deleteXmlTree(rootNode);

    printf("NumberOfProcess = %d\n", input.numberOfProcess);
    printf("InputPrefix = %s\n", input.inputPrefix);
    printf("OutputPrefix = %s\n", input.outputPrefix);
    printf("MaxFileSize = %d\n", input.maxFileSize);

    srand(time(NULL)); /* for generateFile()*/

    pid_t pid;
    char pathFile[300];

    clearDirectory(input.inputPrefix);
    clearDirectory(input.outputPrefix);

    for(int p = 1; p <= input.numberOfProcess; ++p)
    {
        sprintf(pathFile, "%s/input%d", input.inputPrefix, p);

        if(generateFile(pathFile) == -1)
        {
            fprintf(stderr, "Error: generateFile()\n");
            break;
        }

        if((pid = fork()) < 0)
            fprintf(stderr, "Error: fork()\n");
        else if(pid == 0)
        {
            char pid_str[10];
            char maxFileSize_str[10];
            sprintf(pid_str, "%d", getpid());
            sprintf(maxFileSize_str, "%d", input.maxFileSize);
            execl(PATH_PROG, PATH_PROG, pathFile, input.outputPrefix, pid_str, maxFileSize_str, NULL);
        }
    }
}

void clearDirectory(char *pathDir)
{
    DIR *dir = opendir(pathDir);

    if(dir == NULL)
    {
        fprintf(stderr, "Error: clearDirectory()\n");
        return;
    }

    struct dirent *next_file;
    char filepath[300];

    while(next_file = readdir(dir))
    {
        sprintf(filepath, "%s/%s", pathDir, next_file->d_name);
        remove(filepath);
    }

    closedir(dir);
}
