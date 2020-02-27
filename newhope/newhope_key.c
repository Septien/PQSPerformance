/* newhope_key.c
    API
*/

#include <string.h>
#include <openssl/rand.h>
#include <openssl/objects.h>
#include <openssl/err.h>
#include "newhope_locl.h"
#include "newhope_kex.h"

/* Allocate auxiliary variables (context) data structure */
NEWHOPE_CTX *NEWHOPE_CTX_new(const int nid)
{
    NEWHOPE_CTX *ctx;
    ctx = (NEWHOPE_CTX *)OPENSSL_malloc(sizeof(NEWHOPE_CTX)); 
}
