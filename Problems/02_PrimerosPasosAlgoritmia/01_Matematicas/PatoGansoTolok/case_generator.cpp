#include <iostream>
#include <math.h>

#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    long long maxn, n, k;
    std::string c;
    Generator::arguments >> maxn >> c;

    if (c == "par") {
        n = Random::rnd<long long>(1, maxn/2) * 2;
        k = Random::rnd<long long>(1, n/2);
    } else if (c == "pot") {
        long long l = floor(log2(maxn));
        long long l2 = Random::rnd<long long>(0, l);
        n = (long long)1 << l2;
        k = Random::rnd<long long>(1, n);
    } else {
        n = Random::rnd<long long>(1, maxn);
        k = Random::rnd<long long>(1, n);
    }

    Generator::case_in << n << ' ' << k << '\n';

    return 0;
}