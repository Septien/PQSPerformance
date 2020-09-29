/**
 * Performance test, using the number of cycles and seconds metric.
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
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
    struct values *keygenA = NULL, *encA = NULL, *decA = NULL;

    for (i = 0; i < N; i++)
    {
#ifdef TIME
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

#ifdef TIME
    computeMean(N, means, keygen, dec, enc);
#endif
}

void makeTest(int N, struct values **means, struct values **keygen, struct values **dec, struct values **enc, char *file)
{
#ifdef TIME
    measureTimeKEM(N, means, keygen, dec, enc);
#endif
#ifdef MEMORY
    measureTimeKEM(N, NULL, NULL, NULL, NULL);
#endif
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
#ifdef TIME
        printf("Provide the name for the output file: output.csv\n");
#endif
        return 0;
    }

    struct values **keygen, **enc, **dec, **means;
    int N = 1, i, j;
    char *file = NULL;

#ifdef MEMORY
    file = (char *) malloc (8 * sizeof(char));
    memcpy(file, "keys.txt", 8);
    printf("%s", file);
#endif

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

    makeTest(N, means, keygen, dec, enc, file);

#ifdef TIME
    printf("Mean for the KeyGen function:\n\t%f\t%f\n", means[0]->cycles, means[0]->time);
    printf("Mean for the Enc function:\n\t%f\t%f\n", means[1]->cycles, means[1]->time);
    printf("Mean for the Dec function:\n\t%f\t%f\n", means[2]->cycles, means[2]->time);

    FILE *pFile;
    pFile = fopen(argv[1], "w");

    fprintf(pFile, "KeyGen (uS), Enc (uS), Dec (uS)\n");
    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", keygen[i]->time);
    fprintf(pFile, "\n");

    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", enc[i]->time);
    fprintf(pFile, "\n");

    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", dec[i]->time);
    fprintf(pFile, "\n");

    fprintf(pFile, "KeyGen (cycles), Enc (cycles), Dec (cycles)\n");
    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", keygen[i]->cycles);
    fprintf(pFile, "\n");

    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", enc[i]->cycles);
    fprintf(pFile, "\n");

    for (i = 0; i < N - 1; i++)
        fprintf(pFile, "%f,", dec[i]->cycles);
    fprintf(pFile, "\n");

    for (j = 0; j < N; j++)
    {
        free(keygen[j]);
        free(enc[j]);
        free(dec[j]);
    }
    free(keygen);
    free(enc);
    free(dec);
    fclose(pFile);
#endif
#ifdef MEMORY
    free(file);
#endif
    return 0;
}