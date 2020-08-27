#ifndef APIN_H
#define APIN_H

#include "params.h"

#define CRYPTO_SECRETKEYBYTES NTRU_SECRETKEYBYTES
#define CRYPTO_PUBLICKEYBYTES NTRU_PUBLICKEYBYTES
#define CRYPTO_CIPHERTEXTBYTES NTRU_CIPHERTEXTBYTES
#define CRYPTO_BYTES NTRU_SHAREDKEYBYTES

#define CRYPTO_ALGNAME "NTRU-HRSS701"

int crypto_kem_keypairNTRU(unsigned char *pk, unsigned char *sk);

int crypto_kem_encNTRU(unsigned char *ct, unsigned char *ss, const unsigned char *pk);

int crypto_kem_decNTRU(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);


#endif
