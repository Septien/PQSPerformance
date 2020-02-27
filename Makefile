CC = /usr/bin/gcc

LDFLAGS=-L/Users/jash/Documents/Maestria/Tesis/performanceTest/newhope
LIBFLAGS=-lnewhope
PERFFLAGS=-O3 -fomit-frame-pointer -march=native

SOURCES=main.c performance.c
HEADERS=performance.h newhope/api.h

test: $(SOURCES) $(HEADERS)
	$(CC) $(LDFLAGS) $(SOURCES) -o $@ $(LIBFLAGS) $(PERFFLAGS)
