/**
 * Performance test, using the number of cycles metric.
*/

#include <stdlib.h>
#include <stdio.h>

#include "performance.h"

// Crypto libraries
#include "newhope/api.h"

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

void testNewHope(int N, uint64_t *medians)
{
    // For measuring time
    uint64_t t_keygen[N], t_enc[N], t_dec[N];
    int i;

    // For the scheme
    unsigned char pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES], ss[CRYPTO_BYTES], ct[CRYPTO_CIPHERTEXTBYTES];

    for (i = 0; i < N; i++)
    {
        // Key generation
        t_keygen[i] = testKeyGen(crypto_kem_keypair, pk, sk);
        // Encapsulation
        t_enc[i] = testEnc(crypto_kem_enc, ct, ss, pk);
        // Decapsulation
        t_dec[i] = testDec(crypto_kem_dec, ss, ct, sk);
    }

    // Sort arrays
    qsort(t_keygen, sizeof(t_keygen) / sizeof(*t_keygen), sizeof(*t_keygen), comp);
    qsort(t_enc, sizeof(t_enc) / sizeof(*t_enc), sizeof(*t_enc), comp);
    qsort(t_dec, sizeof(t_dec) / sizeof(*t_dec), sizeof(*t_dec), comp);

    // The medians
    medians[0] = t_keygen[(int)N/2];
    medians[1] = t_enc[(int)N/2]; 
    medians[2] = t_dec[(int)N/2];
}

void makeTest(int N, uint64_t *medians)
{
    testNewHope(N, medians);
}

int main(void)
{
    uint64_t *medians;
    medians = (uint64_t *)malloc(3 * sizeof(uint64_t));
    makeTest(1000, medians);
    printf("Median for the KeyGen function:\n\t%llu\n", medians[0]);
    printf("Median for the Enc function:\n\t%llu\n", medians[1]);
    printf("Median for the Dec function:\n\t%llu\n", medians[2]);
    return 0;
}