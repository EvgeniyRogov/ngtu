#include "generator.h"

int getLowerCase()
{
    return 97 + rand() % (122 - 97 + 1);
}

int getUpperCase()
{
    return 66 + rand() % (90 - 66 + 1);
}

int generateFile(char *pathFile)
{
    FILE *file = fopen(pathFile, "w");

    if(file == NULL)
        return -1;

    int words = rand() % MAX_WORDS;
    int letters, spaces;

    for(int i = 0; i < words; ++i)
    {
        letters = 2 + rand() % MAX_LETTERS;
        for(int k = 0; k < letters; ++k)
        {
            if(!k && rand() % 3 == 0)
            {
                fputc(getUpperCase(), file);
                continue;
            }
            fputc(getLowerCase(), file);
        }

        spaces = 1 + rand() % MAX_SPACES;
        for(int k = 0; k < spaces; ++k)
            fputc(' ', file);

        if(i % 5 == 0 && rand() % 2)
            fputc('\n', file); 
    }

    fclose(file);
    return 0;
}