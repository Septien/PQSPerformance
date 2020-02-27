#ifndef PERFORMANCE_H
#define PERFORMANCE_H

#ifdef WIN32
#include <intrin.h>
#else
#include <x86intrin.h>
#endif

uint64_t rdtsc();
uint64_t testKeyGen(int (*keygen)(unsigned char *, unsigned char*), unsigned char *pk, unsigned char *sk);
uint64_t testEnc(int (*enc)(unsigned char*, unsigned char*, const unsigned char*), unsigned char *ct, unsigned char *ss, unsigned char *pk);
uint64_t testDec(int (*dec)(unsigned char*, const unsigned char *, const unsigned char*), unsigned char *ss, unsigned char *ct, unsigned char *sk);

#endif //PERFORMANCE_H