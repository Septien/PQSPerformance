#CC = clang
CC = gcc
LDFLAGS = -lcrypto

SOURCES = aes256ctr.c Decode.c Encode.c int32.c kat_kem.c kem.c nist/rng.c sha512.c uint32.c uint32_sort.c
SOURCESLIB = aes256ctr.c Decode.c Encode.c int32.c kem.c nist/rng.c sha512.c uint32.c uint32_sort.c
HEADERS = aes256ctr.h api.h crypto_kem.h crypto_kem_ntrulpr653.h Decode.h Encode.h int16.h int32.h int8.h params.h paramsmenu.h randombytes.h nist/rng.h sha512.h uint16.h uint32.h uint64.h
FLAGSPIC = -c -Wall -march=native -mtune=native -O3 -fomit-frame-pointer -fwrapv
FLAGSLIB = -dynamiclib -shared

.PHONY: clean, libntru-prime

libntru-prime: ntru-primelib
	$(CC) $(FLAGSLIB) -o libntru-prime.so *.o  $(LDFLAGS)

ntru-primelib: $(SOURCESLIB) $(HEADERS)
	$(CC) $(FLAGSPIC) $(SOURCESLIB) -fpic

clean:
	-rm *.o
