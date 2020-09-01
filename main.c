/**
 * Performance test, using the number of cycles metric.
*/

#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>

#include "performance.h"

// Crypto libraries
#ifdef NTRU
#include "ntru-hrss701/api.h"
#endif

#ifdef NTRUP
#include "ntrulpr653/api.h"
#include "ntrulpr653/crypto_kem.h"
#endif

#ifdef SABER
#include "saber/api.h"
#endif

#ifdef  KYBER
#include "kyber/api.h"
#endif

#ifdef FRODO
#include "FrodoKEM-640/api.h"
#endif

#ifdef RPI
#define uint64_t u_int64_t
#endif

void computeMean(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
    means[0]->cycles = means[0]->time = 0;
    means[1]->cycles = means[1]->time = 0;
    means[2]->cycles = means[2]->time = 0;
    for (int i = 0; i < N; i++)
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

void testKEM(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
    // For measuring time
    int i;

    struct values *keygenA = NULL, *encA = NULL, *decA = NULL;

    // For the scheme
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

       for (i = 0; i < N; i++)
    {
#ifndef MEMORY
        keygenA = keygen[i];
        encA = enc[i];
        decA = dec[i];
#endif
        // Key generation
        testKeyGen(crypto_kem_keypair, pk, sk, keygenA);
        // Encapsulation
        testEnc(crypto_kem_enc, ct, ss, pk, encA);
        // Decapsulation
        testDec(crypto_kem_dec, ss, ct, sk, decA);
    }

#ifndef MEMORY
    computeMean(N, means, keygen, dec, enc);
#endif
}

void makeTest(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
    testKEM(N, means, keygen, dec, enc);
}

int main(int argc, char **argv)
{
#ifndef MEMORY
    if (argc < 2)
    {
        printf("Provide the name for the output file: output.csv\n");
        return 0;
    }
#endif

    struct values **keygen, **enc, **dec, **means;
    int N = 1, i, j;
    int m[1000];
    for (i = 0; i < 1000; i++)
        m[i] = i;

#ifndef MEMORY
    N = 2000;
    keygen = (struct values **)malloc(N * sizeof(struct values *));
    enc = (struct values **)malloc(N * sizeof(struct values *));
    dec = (struct values **)malloc(N * sizeof(struct values *));
    means = (struct values **)malloc(3 * sizeof(struct values *));

    /* Allocate memory for each entry */
    for (j = 0; j < N; j++)
    {
        keygen[j] = (struct values *) malloc (sizeof(struct values));
        enc[j] = (struct values *) malloc (sizeof(struct values));
        dec[j] = (struct values *) malloc (sizeof(struct values));
    }
    means[0] = (struct values *)malloc(sizeof(struct values));
    means[1] = (struct values *)malloc(sizeof(struct values));
    means[2] = (struct values *)malloc(sizeof(struct values));
#endif

#ifdef RPI    
    init_module();
#endif

    makeTest(N, means, keygen, dec, enc);

#ifndef MEMORY
    printf("Mean for the KeyGen function:\n\t%f\t%f\n", means[0]->cycles, means[0]->time);
    printf("Mean for the Enc function:\n\t%f\t%f\n", means[1]->cycles, means[1]->time);
    printf("Mean for the Dec function:\n\t%f\t%f\n", means[2]->cycles, means[2]->time);

    FILE *pfile;
    pfile = fopen(argv[1], "w");
    fprintf(pfile, "KeyGen (uS), Enc (uS), Dec (uS), KeyGen (cycles), Enc (cycles), Dec (cycles)\n");
    fprintf(pfile, "%f, %f, %f, %f, %f, %f\n", means[0]->time, means[1]->time, means[2]->time, means[0]->cycles, means[1]->cycles, means[2]->cycles);
    for (int i = 0; i < N-1; i++)
    {
        fprintf(pfile, "%f, %f, %f, %f, %f, %f\n", keygen[i]->time, enc[i]->time, dec[i]->time, keygen[i]->cycles, enc[i]->cycles, dec[i]->cycles);
    }
#endif
    return 0;
}