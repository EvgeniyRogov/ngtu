#include <stdio.h>
#include <ctype.h> 
#include <time.h>

int countWords(char *pathFile);
int getFileSize(char *pathFile);

int main(int argc, char *argv[])
{
    if(argc != 5)
    {
        fprintf(stderr, "Error wordcounter: not enough arguments\n");
        return 1;
    }

    char *pathFile = argv[1];
    char *outputPrefix = argv[2];
    char *pid_str = argv[3];
    char *maxFileSize_str = argv[4];

    char fileInfo[200];
    char pathOutputFile[100];
    char error[50];

    sprintf(pathOutputFile, "%s/output%s", outputPrefix, pid_str);

    FILE* fileOutput = fopen(pathOutputFile, "w");

    if(fileOutput == NULL)
    {
        fprintf(stderr, "Error: fileOutput is not opened\n");
        return 1;
    }

    int size = getFileSize(pathFile);

    if(size == -1)
    {
        fprintf(stderr, "Error: getFileSize()\n");
        return 1; 
    }
    else if(size > 1000)
        sprintf(error, "excess MaxFileSize");
    else
        sprintf(error, "");

    clock_t begin_time = clock();
    int count = countWords(pathFile);
    clock_t end_time = clock();
    double spent_time = (double)(end_time - begin_time) / CLOCKS_PER_SEC;

    if(count == -1)
    {
        fprintf(stderr, "Error: countWords()\n");
        return 1;  
    }

    sprintf(fileInfo, "Name: %s\nCount: %d\nPid: %s\nTime: %lf\nError: %s\n", pathFile, count, pid_str, spent_time, error);
    fputs(fileInfo, fileOutput);
    fclose(fileOutput);

    return 0;
}

int countWords(char *pathFile)
{
    FILE *file = fopen(pathFile, "r");

    if(file == NULL)
        return -1;

    int c;
    int words = 0;
    int letters = 0;

    for(;;)
    {
        c = fgetc(file);

        if(isalpha(c))
        {
            ++letters;
            continue;
        }

        if(letters >= 2 && (isspace(c) || c == EOF)) 
            ++words;

        letters = 0;

        if(c == EOF)
            break;
    }

    fclose(file);
    return words;
}

int getFileSize(char *pathFile)
{
    FILE *file = fopen(pathFile, "r");

    if(file == NULL)
        return -1;

    fseek(file, 0, SEEK_END); 
    int size = ftell(file);
    fseek(file, 0, SEEK_SET);

    fclose(file);

    return size;
}