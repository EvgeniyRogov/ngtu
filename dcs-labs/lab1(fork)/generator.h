#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define MAX_FILES 10
#define MAX_WORDS 100
#define MAX_LETTERS 15
#define MAX_SPACES 4

static int getLowerCase();
static int getUpperCase();
int generateFile(char *pathFile);