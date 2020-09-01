CC = gcc
AR = ar rcs

SOURCESLIB = verify.c sample.c rng.c poly.c packq.c pack3.c owcpa.c kem.c fips202.c 
HEADERS = verify.h sample.h rng.h poly.h params.h owcpa.h kem.h fips202.h api.h 
FLAGSPIC = -c -Wall -march=native -mtune=native -O3 -fomit-frame-pointer -fwrapv

.PHONY: clean, ntruO

ntruO: $(SOURCESLIB) $(HEADERS)
	$(CC) $(FLAGSPIC) $(SOURCESLIB) -fpic

clean:
	-rm *.o
