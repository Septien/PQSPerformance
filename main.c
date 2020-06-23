/**
 * Performance test, using the number of cycles metric.
*/

#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>

#include "performance.h"

// Crypto libraries


#ifdef RPI
#define uint64_t u_int64_t
#endif

/*
*   Comparison function.
*   https://stackoverflow.com/questions/1787996/c-library-function-to-perform-sort
*/
int comp(const void *elem1, const void *elem2)
{
    int f = *((int*)elem1);
    int s = *((int*)elem2);
    if (f > s) return 1;
    if (s < f) return -1;
    return 0;
}

void testNewHope(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
//#include "newhope/api.h"
    // For measuring time
    int i;

    // For the scheme
   /* unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

   for (i = 0; i < N; i++)
    {
        // Key generation
        testKeyGen(crypto_kem_keypair, pk, sk, keygen[i]);
        // Encapsulation
        testEnc(crypto_kem_enc, ct, ss, pk, enc[i]);
        // Decapsulation
        testDec(crypto_kem_dec, ss, ct, sk, dec[i]);
    }

    means[0]->cycles = means[0]->time = 0;
    means[1]->cycles = means[1]->time = 0;
    means[2]->cycles = means[2]->time = 0;
    for (i = 0; i < N; i++)
    {
        means[0]->cycles += keygen[i]->cycles;
        means[0]->time += keygen[i]->time;
        means[1]->cycles += enc[i]->cycles;
        means[1]->time += enc[i]->time;
        means[2]->cycles += dec[i]->cycles;
        means[2]->time += dec[i]->time;
    }
    means[0]->cycles /= N;
    means[0]->time /= N;
    means[1]->cycles /= N;
    means[1]->time /= N;
    means[2]->cycles /= N;
    means[2]->time /= N;*/
}

void testNTRU(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
/*#include "ntru/api.h"
    // For measuring time
    int i;

    // For the scheme
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

       for (i = 0; i < N; i++)
    {
        // Key generation
        testKeyGen(crypto_kem_keypair, pk, sk, keygen[i]);
        // Encapsulation
        testEnc(crypto_kem_enc, ct, ss, pk, enc[i]);
        // Decapsulation
        testDec(crypto_kem_dec, ss, ct, sk, dec[i]);
    }

    means[0]->cycles = means[0]->time = 0;
    means[1]->cycles = means[1]->time = 0;
    means[2]->cycles = means[2]->time = 0;
    for (i = 0; i < N; i++)
    {
        means[0]->cycles += keygen[i]->cycles;
        means[0]->time += keygen[i]->time;
        means[1]->cycles += enc[i]->cycles;
        means[1]->time += enc[i]->time;
        means[2]->cycles += dec[i]->cycles;
        means[2]->time += dec[i]->time;
    }
    means[0]->cycles /= N;
    means[0]->time /= N;
    means[1]->cycles /= N;
    means[1]->time /= N;
    means[2]->cycles /= N;
    means[2]->time /= N;*/
}

void testNTRUprime(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
/*#include "ntru-prime/api.h"
#include "ntru-prime/crypto_kem.h"
    // For measuring time
    int i;

    // For the scheme
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

       for (i = 0; i < N; i++)
    {
        // Key generation
        testKeyGen(crypto_kem_keypair, pk, sk, keygen[i]);
        // Encapsulation
        testEnc(crypto_kem_enc, ct, ss, pk, enc[i]);
        // Decapsulation
        testDec(crypto_kem_dec, ss, ct, sk, dec[i]);
    }

    means[0]->cycles = means[0]->time = 0;
    means[1]->cycles = means[1]->time = 0;
    means[2]->cycles = means[2]->time = 0;
    for (i = 0; i < N; i++)
    {
        means[0]->cycles += keygen[i]->cycles;
        means[0]->time += keygen[i]->time;
        means[1]->cycles += enc[i]->cycles;
        means[1]->time += enc[i]->time;
        means[2]->cycles += dec[i]->cycles;
        means[2]->time += dec[i]->time;
    }
    means[0]->cycles /= N;
    means[0]->time /= N;
    means[1]->cycles /= N;
    means[1]->time /= N;
    means[2]->cycles /= N;
    means[2]->time /= N;*/
}

void testSaber(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
#include "saber/api.h"
    // For measuring time
    int i;

    // For the scheme
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

       for (i = 0; i < N; i++)
    {
        // Key generation
        testKeyGen(crypto_kem_keypair, pk, sk, keygen[i]);
        // Encapsulation
        testEnc(crypto_kem_enc, ct, ss, pk, enc[i]);
        // Decapsulation
        testDec(crypto_kem_dec, ss, ct, sk, dec[i]);
    }

    means[0]->cycles = means[0]->time = 0;
    means[1]->cycles = means[1]->time = 0;
    means[2]->cycles = means[2]->time = 0;
    for (i = 0; i < N; i++)
    {
        means[0]->cycles += keygen[i]->cycles;
        means[0]->time += keygen[i]->time;
        means[1]->cycles += enc[i]->cycles;
        means[1]->time += enc[i]->time;
        means[2]->cycles += dec[i]->cycles;
        means[2]->time += dec[i]->time;
    }
    means[0]->cycles /= N;
    means[0]->time /= N;
    means[1]->cycles /= N;
    means[1]->time /= N;
    means[2]->cycles /= N;
    means[2]->time /= N;
}

void makeTest(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
    //estNewHope(N, means, keygen, dec, enc);
    //testNTRU(N, means, keygen, dec, enc);
    //testNTRUprime(N, means, keygen, dec, enc);
    testSaber(N, means, keygen, dec, enc);
}

int main(void)
{

    struct values **keygen, **enc, **dec, **means;
    int N = 2000;
    keygen = (struct values **)malloc(N * sizeof(struct values *));
    enc = (struct values **)malloc(N * sizeof(struct values *));
    dec = (struct values **)malloc(N * sizeof(struct values *));
    means = (struct values **)malloc(3 * sizeof(struct values *));

    /* Allocate memory for each entry */
    for (int i = 0; i < N; i++)
    {
        keygen[i] = (struct values *) malloc (sizeof(struct values));
        enc[i] = (struct values *) malloc (sizeof(struct values));
        dec[i] = (struct values *) malloc (sizeof(struct values));
    }
    means[0] = (struct values *)malloc(sizeof(struct values));
    means[1] = (struct values *)malloc(sizeof(struct values));
    means[2] = (struct values *)malloc(sizeof(struct values));
    
#ifdef RPI    
    init_module();
#endif

    makeTest(2000, means, keygen, dec, enc);

    printf("Mean for the KeyGen function:\n\t%f\t%f\n", means[0]->cycles, means[0]->time);
    printf("Mean for the Enc function:\n\t%f\t%f\n", means[1]->cycles, means[1]->time);
    printf("Mean for the Dec function:\n\t%f\t%f\n", means[2]->cycles, means[2]->time);

    int i;
    //FILE *pfile;
    /*pfile = fopen("timemeasure.csv", "w");
    fprintf(pfile, "%lu, %lu, %lu\n", medians[0], medians[1], medians[2]);
    for (int i = 0; i < N-1; i++)
    {
        fprintf(pfile, "%lu,%lu,%lu\n", keygen[i], enc[i], dec[i]);
    }*/
    return 0;
}