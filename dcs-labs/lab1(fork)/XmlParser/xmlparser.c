#include <stdio.h>
#include <ctype.h> 
#include <stdlib.h>
#include <string.h>

#include "xmlparser.h"

void insertChild(XmlNode* curNode, XmlNode* xmlNode)
{
    if(!curNode->childs)
    {
        curNode->childs = (XmlList*)malloc(sizeof(XmlList));
        ListNode* newNode = (ListNode*)malloc(sizeof(ListNode));
        newNode->xmlNode = xmlNode;
        curNode->childs->root = newNode;
        return;
    }

    XmlList *xmlList = curNode->childs;
    ListNode* listNode = xmlList->root;

    while(listNode->next)
        listNode = listNode->next;

    listNode->next = (ListNode*)malloc(sizeof(ListNode));
    ListNode *newNode = listNode->next;
    newNode->prev = listNode;
    newNode->xmlNode = xmlNode;
}

XmlNode* createXmlTree(const char *pathFile)
{
    FILE *xmlFile = fopen(pathFile, "r");
    if(xmlFile == NULL)
        return NULL;

    XmlNode *curNode = NULL;
    XmlNode *rootNode = NULL;
    State state = AFTER_CLOSE_TAG;

    int c;
    int i_content;
    int i_tagName;
    char *closeTag = NULL;
    int flagRequest = 0;
    int flagOpen = 0;

    while((c = fgetc(xmlFile)) != EOF)
    {
        if(state == AFTER_CLOSE_TAG)
        {
            if(isspace(c))
                continue;
            else if(c == '<')
            {
                flagRequest = 1;
                flagOpen = 1;
                state = OPEN_TAG;    
            }
            else
                break;
        }
        else if(state == OPEN_TAG)
        {
            if(c == '/' && flagOpen)
                state = CLOSE_TAG;
            else if(c == '>')
                state = CONTENT;
            else if(c == '<')
                break;
            else
            {
                if(flagRequest && !curNode)
                {
                    rootNode = (XmlNode*)malloc(sizeof(XmlNode));
                    curNode = rootNode;
                    flagRequest = 0;
                }
                else if(flagRequest && curNode)
                {
                    XmlNode* newNode = (XmlNode*)malloc(sizeof(XmlNode));
                    newNode->parent = curNode;
                    insertChild(curNode, newNode);
                    curNode = newNode;
                    flagRequest = 0;
                } 

                if(curNode->parent && curNode->parent->content)
                {
                    free(curNode->parent->content);
                    curNode->parent->content = NULL;
                }

                if(!curNode->tagName)
                {
                    curNode->tagName = (char*)malloc(sizeof(char) * 100);
                    i_tagName = 0;
                }
                curNode->tagName[i_tagName++] = c;
            }
            flagOpen = 0;
        }
        else if(state == CLOSE_TAG)
        {
            if(c == '>')
            {
                if(strcmp(curNode->tagName, closeTag) == 0)
                {
                    curNode = curNode->parent;
                    free(closeTag);
                    closeTag = NULL;
                    state = AFTER_CLOSE_TAG;
                }
                else
                    break;
            }
            else if(c == '<')
                break;
            else
            {
                if(!closeTag)
                {
                    closeTag = (char*)malloc(sizeof(char) * 100);
                    i_tagName = 0; 
                }
                closeTag[i_tagName++] = c; 
            }   
        }
        else if(state == CONTENT)
        {
            if(c == '<')
            {
                flagRequest = 1;
                flagOpen = 1;
                state = OPEN_TAG;
            }
            else if(c == '>')
                break;
            else
            {
                if(!curNode->content)
                {
                    curNode->content = (char*)malloc(sizeof(char) * 1000);
                    i_content = 0;
                } 
                curNode->content[i_content++] = c;
            }
        }
    }

    fclose(xmlFile);

    if(curNode)
    {
        deleteXmlTree(rootNode);
        return NULL;
    }

    return rootNode;
}

void getContent(XmlNode* xmlNode, const char* tag, char* content)
{
    if(!xmlNode || !tag || !content)
    {
        fprintf(stderr, "Error: getContent()\n");
        return;
    }

    if(strcmp(xmlNode->tagName, tag) == 0)
    {
        if(xmlNode->content)
            strcpy(content, xmlNode->content);
        return;
    }

    XmlList *xmlList = xmlNode->childs;
    if(xmlList == NULL) return;
    ListNode *listNode = xmlList->root;

    while(listNode)
    {
        if(!strcmp(listNode->xmlNode->tagName, tag) && !listNode->xmlNode->content)
        {
            strcpy(content, listNode->xmlNode->content);
            return;
        }
        getContent(listNode->xmlNode, tag, content);
        listNode = listNode->next;
    }
}

void deleteXmlTree(XmlNode* xmlNode)
{
    XmlList *xmlList = xmlNode->childs;
    if(xmlList == NULL)
    {
        free(xmlNode->tagName);
        free(xmlNode->content);
        free(xmlNode);
        return;
    }

    ListNode *listNode = xmlList->root;
    while(listNode)
    {
        deleteXmlTree(listNode->xmlNode);
        ListNode* tempNode = listNode;
        listNode = listNode->next;
        free(tempNode);
    }
    free(xmlList);
    free(xmlNode->tagName);
    free(xmlNode->content);
    free(xmlNode);
}
