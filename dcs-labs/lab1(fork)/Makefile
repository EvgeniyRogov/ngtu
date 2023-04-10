CC = gcc
PROG_NAME = lab1
WORDCOUNTER = wordcounter

$(PROG_NAME) : main.c generator.c XmlParser/xmlparser.c
	$(CC) $^ -o $@ -g

$(WORDCOUNTER) : wordcounter.c
	$(CC) $^ -o $@ -g