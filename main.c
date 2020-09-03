/**
 * Performance test, using the number of cycles metric.
*/

#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>

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

#include "performance.h"

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

void measureTimeKEM(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc)
{
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

    computeMean(N, means, keygen, dec, enc);
}

void measureMemoryKeyGen(char *file)
{
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES];
    // Key generation
    testKeyGen(crypto_kem_keypair, pk, sk, NULL);

    FILE *fd;
    fd = fopen(file, "w");
    fprintf(fd, "%s\n%s\n", pk, sk);
    fclose(fd);
}

void measureMemoryEnc(char *file)
{
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];
    FILE *fd;
    fd = fopen(file, "rw");
    fscanf(fd, "%s", pk);
    testEnc(crypto_kem_enc, ct, ss, pk, NULL);
    fprintf(fd, "%s\n", ct);
    fclose(fd);
}

void measureMemoryDec(char *file)
{
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];
    FILE *fd;
    fd = fopen(file, "r");
    fscanf(fd, "%s", pk);
    fscanf(fd, "%s", sk);
    fscanf(fd, "%s", ct);
    testDec(crypto_kem_dec, ss, ct, sk, NULL);
    fclose(fd);
}


void makeTest(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc, char *file)
{
#ifdef TIME
    measureTimeKEM(N, means, keygen, dec, enc);
#endif
#ifdef MEMORY
    #ifdef KEYGEN
        measureMemoryKeyGen(file);
    #elif ENC
        measureMemoryEnc(file);
    #elif DEC
        measureMemoryDec(file);
    #else // All
        measureMemoryKeyGen(file);
        measureMemoryEnc(file);
        measureMemoryDec(file);
    #endif
#endif
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
#ifdef TIME
        printf("Provide the name for the output file: output.csv\n");
#elif MEMORY
        printf("Provide the name for the keys file: keys.txt\n");
#endif
        return 0;
    }

    struct values **keygen, **enc, **dec, **means;
    int N = 1, i, j;

#ifdef TIME
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

    makeTest(N, means, keygen, dec, enc, argv[2]);

#ifdef TIME
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