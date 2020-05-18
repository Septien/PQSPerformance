#include "performance.h"
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>

#ifdef RPI
#include <linux/module.h>
#include <linux/kernel.h>

#define uint64_t u_int64_t
#endif

/*
*   Get the current number of cycles.
*/
FUNC rdtsc()
{
#ifndef RPI
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t) hi << 32 | lo);
#else
    struct timespec time;
    clock_gettime(CLOCK_REALTIME, &time);
    return (uint64_t)(time.tv_sec*1e9 + time.tv_nsec);
#endif
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