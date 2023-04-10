CC = g++
SERVER = server
TEST = test

$(SERVER) : server.cpp
	$(CC) $^ -o $@ -g -pthread

$(TEST) : test.cpp
	$(CC) $^ -o $@ -g -pthread