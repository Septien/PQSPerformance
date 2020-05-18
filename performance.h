#ifndef PERFORMANCE_H
#define PERFORMANCE_H

#include <sys/types.h>
#include <time.h>

#ifndef RPI
    #ifdef WIN32
    #include <intrin.h>
    #else
    #include <x86intrin.h>
    #endif
    #define FUN uint64_t
#else
#include <linux/module.h>
#include <linux/kernel.h>
#define uint64_t u_int64_t
#define FUNC static inline uint64_t
#endif

#ifdef RPI
int init_module(void); 
void cleanup_module(void);
#endif
FUNC rdtsc();
uint64_t testKeyGen(int (*keygen)(unsigned char *, unsigned char*), unsigned char *pk, unsigned char *sk);
uint64_t testEnc(int (*enc)(unsigned char*, unsigned char*, const unsigned char*), unsigned char *ct, unsigned char *ss, unsigned char *pk);
uint64_t testDec(int (*dec)(unsigned char*, const unsigned char *, const unsigned char*), unsigned char *ss, unsigned char *ct, unsigned char *sk);

#endif //PERFORMANCE_H