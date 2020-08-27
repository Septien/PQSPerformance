#ifndef NTRUKEM_H
#define NTRUKEM_H

int crypto_kem_keypairNTRU(unsigned char *pk, unsigned char *sk);

int crypto_kem_encNTRU(unsigned char *c, unsigned char *k, const unsigned char *pk);

int crypto_kem_decNTRU(unsigned char *k, const unsigned char *c, const unsigned char *sk);

#endif
