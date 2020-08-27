#ifndef APIK_H
#define APIK_H

#include "params.h"

#define CRYPTO_SECRETKEYBYTES  KYBER_SECRETKEYBYTES
#define CRYPTO_PUBLICKEYBYTES  KYBER_PUBLICKEYBYTES
#define CRYPTO_CIPHERTEXTBYTES KYBER_CIPHERTEXTBYTES
#define CRYPTO_BYTES           KYBER_SSBYTES

#if   (KYBER_K == 2)
#define CRYPTO_ALGNAME "Kyber512"
#elif (KYBER_K == 3)
#define CRYPTO_ALGNAME "Kyber768"
#elif (KYBER_K == 4)
#define CRYPTO_ALGNAME "Kyber1024"
#else
#error "KYBER_K must be in {2,3,4}"
#endif

int crypto_kem_keypairKYBER(unsigned char *pk, unsigned char *sk);

int crypto_kem_encKYBER(unsigned char *ct, unsigned char *ss, const unsigned char *pk);

int crypto_kem_decKYBER(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);


#endif
