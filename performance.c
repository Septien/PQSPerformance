#include "performance.h"

/*
*   Get the current number of cycles.
*/
uint64_t rdtsc()
{
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t) hi << 32 | lo);
}

uint64_t testKeyGen(int (*keygen)(unsigned char *, unsigned char*), unsigned char *pk, unsigned char *sk)
{
    uint64_t low, high;
    low = rdtsc();
    keygen(pk, sk);
    high = rdtsc();
    return high - low;
}

uint64_t testEnc(int (*enc)(unsigned char*, unsigned char*, const unsigned char*), unsigned char *ct, unsigned char *ss, unsigned char *pk)
{
    uint64_t low, high;
    low = rdtsc();
    enc(ct, ss, pk);
    high = rdtsc();
    return high - low;
}

uint64_t testDec(int (*dec)(unsigned char*, const unsigned char *, const unsigned char*), unsigned char *ss, unsigned char *ct, unsigned char *sk)
{
    uint64_t low, high;
    low = rdtsc();
    dec(ss, ct, sk);
    high = rdtsc();
    return high - low;
}