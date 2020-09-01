import os

ciphers = ["NTRU=1", "SABER=1", "KYBER=1", "FRODO=1"]
massiffile = ["ntru.out", "saber.out", "kyber.out", "frodo.out"]
rm = "rm test"
make = "make test "
valgrind = "valgrind --tool=massif --heap=yes --time-unit=B --massif-out-file="

for i in range(4):
    print(ciphers[i])
    # Remove test binary
    cmd = rm
    os.system(cmd)

    # make with the memory option enabled
    cmd = make + ciphers[i] + " MEMORY=1"
    os.system(cmd)

    cmd = "size test"
    os.system(cmd)
    # Profile with valgrind
    #cmd = valgrind + massiffile[i] + " ./test"
    #os.system(cmd)
