typedef struct XmlList
{
    struct ListNode* root;
} XmlList;

typedef struct ListNode
{
    struct XmlNode *xmlNode;
    struct ListNode *next;
    struct ListNode *prev;
} ListNode;

typedef struct XmlNode
{
    char *tagName;
    char *content;
    struct XmlNode* parent;
    struct XmlList* childs;
} XmlNode;

typedef enum{AFTER_CLOSE_TAG, OPEN_TAG, CLOSE_TAG, CONTENT} State;

XmlNode* createXmlTree(const char *pathFile);
void deleteXmlTree(XmlNode* xmlNode);
void getContent(XmlNode* nodeRoot, const char* tag, char* content);
void insertChild(XmlNode* curNode, XmlNode* xmlNode);
