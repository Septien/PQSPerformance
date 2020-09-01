CC = /usr/bin/gcc

# -fomit-frame-pointer
PERFFLAGS=-O3 -march=native -Xlinker -Map=output.map -pg 
CFLAGS= #-DRPI #For the raspberry pi

SOURCES=main.c

# Which cryptosystem to include?
HEADERS=
OBJS=
ifdef NTRU
	include = ntru-hrss701/Makefile
	sourcesO = $(shell cd ntru-hrss701/ && find -iname '*.c' | sed 's/\.c/.o/g')
	OBJS = $(patsubst %.o, ntru-hrss701/%.o, $(sourcesO))
	HEADERS += ntru-hrss701/api.h
	CFLAGS += -DNTRU
endif
ifdef NTRUP
	include = ntrulpr653/Makefile
	sourcesO = $(shell cd ntrulpr653/ && find -iname '*.c' | sed 's/\.c/.o/g')
	OBJS = $(patsubst %.o, ntrulpr653/%.o, $(sourcesO))
	HEADERS += ntrulpr653/api.h ntrulpr653/crypto_kem.h
	CFLAGS += -DNTRUP
endif
ifdef SABER
	include saber/Makefile
	sourcesO = $(shell cd saber/ && find -iname '*.c' | sed 's/\.c/.o/g')
	OBJS = $(patsubst %.o, saber/%.o, $(sourcesO))
	HEADERS += saber/api.h
	CFLAGS += -DSABER
endif
ifdef KYBER
	include = kyber/Makefile
	sourcesO = $(shell cd kyber/ && find -iname '*.c' | sed 's/\.c/.o/g')
	OBJS = $(patsubst %.o, kyber/%.o, $(sourcesO))
	HEADERS += kyber/api.h
	CFLAGS += -DKYBER
endif
ifdef FRODO
	inlude = FrodoKEM-640/Makefile
	$(OBJS) = $(patsubst %.o, FrodoKEM-640/%.o, *.o)
	HEADERS += FrodoKEM-640/api.h
	CFLAGS += -DFRODO
endif
LIBFLAGS += -lcrypto

DEBUGF=
ifdef MEMORY
	DEBUGF = -g
	CFLAGS += -DMEMORY
endif

$( info $(LIBFLAGS) )
performance.o : performance.h performance.c
	$(CC) -c performance.c

test: $(SOURCES) $(HEADERS) performance.o $(OBJS)
	$(CC) $(DEBUGF) $(CFLAGS) $(SOURCES) performance.o -o $@ $(OBJS) $(LIBFLAGS) $(PERFFLAGS)

clean:
	rm test
