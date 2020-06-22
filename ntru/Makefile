#CC = clang
CC = gcc
LDFLAGS = -lcrypto

SOURCES = crypto_sort.c fips202.c kem.c owcpa.c pack3.c packq.c poly.c PQCgenKAT_kem.c rng.c sample.c verify.c
SOURCESLIB = crypto_sort.c fips202.c kem.c owcpa.c pack3.c packq.c poly.c rng.c sample.c verify.c
HEADERS = api.h crypto_sort.h fips202.h kem.h owcpa.h params.h poly.h rng.h sample.h verify.h 
FLAGSPIC = -c -Wall -march=native -mtune=native -O3 -fomit-frame-pointer -fwrapv
FLAGSLIB = -dynamiclib -shared
#FLAGSLIB = -shared

PQCgenKAT_kem: $(SOURCES) $(HEADERS)
	$(CC) $(SOURCES) -o $@ $(LDFLAGS)

.PHONY: clean, libntru

libntru: ntrulib
	$(CC) $(FLAGSLIB) -o libntru.so *.o  $(LDFLAGS)

ntrulib: $(SOURCESLIB) $(HEADERS)
	$(CC) $(FLAGSPIC) $(SOURCESLIB) -fpic

clean:
	-rm PQCgenKAT_kem *.o
