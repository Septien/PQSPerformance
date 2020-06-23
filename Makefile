CC = /usr/bin/gcc

LDFLAGS=-L/media/phantom/Data/Crypto/PQSPerformance#/home/pi/Documents/Maestria/Tesis/PQSPerformance#/Users/jash/Documents/Maestria/Tesis/performanceTest/newhope
LIBFLAGS=-lnewhope -lntru -lntru-prime
PERFFLAGS=-O3 -fomit-frame-pointer -march=native
CFLAGS= #-DRPI #For the raspberry pi

SOURCES=main.c performance.c
HEADERS=performance.h newhope/api.h ntru/api.h

test: $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) -o $@ $(LIBFLAGS) $(PERFFLAGS)
