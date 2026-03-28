#include <iostream>

#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    int N, Q, maxai;
    std::string tipo;
    Generator::arguments >> N >> Q >> maxai >> tipo;

    auto vec = Random::rnd(1, maxai, N);
    Generator::case_in << N << '\n';
    for (auto& it : vec)
        Generator::case_in << it << ' ';
    Generator::case_in << '\n';

    Generator::case_in << Q << '\n';
    while (Q--) {
        int a = Random::rnd(1, 2);
        if (tipo != "RAND") a = 1;
        int l, r;
        if (a == 1) {
            l = Random::rnd(1, N);
            r = Random::rnd(1, N);
            if (r < l) std::swap(l, r);
            if (tipo == "PREFIX") l = 1;
        } else {
            l = Random::rnd(1, N);
            r = Random::rnd(1, maxai);
        }
        Generator::case_in << a << ' ' << l << ' ' << r << '\n';
    }

    return 0;
}