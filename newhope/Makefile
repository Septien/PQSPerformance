#CC = clang
CC = /usr/bin/gcc
LDFLAGS = -lcrypto

SOURCES = kem.c cpapke.c fips202.c ntt.c poly.c precomp.c reduce.c rng.c verify.c PQCgenKAT_kem.c
SOURCESLIB = kem.c cpapke.c fips202.c ntt.c poly.c precomp.c reduce.c rng.c verify.c newhope.c
HEADERS = api.h cpapke.h fips202.h ntt.h params.h poly.h reduce.h rng.h verify.h
FLAGSPIC = -c -Wall -march=native -mtune=native -O3 -fomit-frame-pointer -fwrapv
FLAGSLIB = -dynamiclib -shared
#FLAGSLIB = -shared

PQCgenKAT_kem: $(SOURCES) $(HEADERS)
	$(CC) $(SOURCES) -o $@ $(LDFLAGS)

.PHONY: clear, libnewhope

libnewhope: newhopelib
	#$(CC) $(FLAGSLIB) -W1,soname,libnewhope.so -fvisibility=hidden -o libnewhope.dylib *.o  $(LDFLAGS)
	$(CC) $(FLAGSLIB) -o libnewhope.so *.o  $(LDFLAGS)

newhopelib: $(SOURCESLIB) $(HEADERS)
	$(CC) $(FLAGSPIC) $(SOURCESLIB) -fpic

clean:
	-rm PQCgenKAT_kem *.o
