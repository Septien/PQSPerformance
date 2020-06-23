#CC = clang
CC = gcc
LDFLAGS = -lcrypto

SOURCESLIB = pack_unpack.c poly.c rng.c fips202.c verify.c cbd.c SABER_indcpa.c kem.c
HEADERS = SABER_params.h pack_unpack.h poly.h rng.h fips202.h verify.h cbd.h SABER_indcpa.h kem.h 
FLAGSPIC = -c -Wall -march=native -mtune=native -O3 -fomit-frame-pointer -fwrapv
FLAGSLIB = -dynamiclib -shared

.PHONY: clean, libntru

libsaber: saberlib
	$(CC) $(FLAGSLIB) -o libsaber.so *.o  $(LDFLAGS) -fPIC

saberlib: $(SOURCESLIB) $(HEADERS)
	$(CC) $(FLAGSPIC) $(SOURCESLIB) -fPIC

clean:
	-rm *.o
