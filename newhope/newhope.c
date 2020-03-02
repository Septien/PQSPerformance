#include <time.h>
#include <stdlib.h>

#include "newhope.h"
#include "api.h"
#include "rng.h"
#include "cpapke.h"

// Define which functions are made visible to the client
#define EXPORT __attribute__((visibility("default")))

EXPORT
void KeyGen(unsigned char *pk, unsigned char *sk)
{
    cpapke_keypair(pk, sk);
}

/*
*   TODO: Set as input "n"
*/
EXPORT
void encrypt(unsigned char *ct, unsigned char *m, unsigned char *pk)
{
    // Generate a random sequence of bytes each time
    srand(time(NULL));
    unsigned int n = (unsigned int) (rand() % 65535);
    unsigned char z[n];
    randombytes(z, n);
    cpapke_enc(ct, m, pk, z);
}

EXPORT
void decrypt(unsigned char *m, unsigned char *ct, unsigned char *sk)
{
    cpapke_dec(m, ct, sk);
}
