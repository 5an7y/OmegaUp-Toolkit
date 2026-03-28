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
    int N, maxci, maxri;
    std::string tipo;
    Generator::arguments >> N >> maxci >> maxri >> tipo;

    std::vector<int> cis(N), ris(N);
    if (tipo == "RAND") {
        cis = Random::rnd(1, maxci, N);
        ris = Random::rnd(1, maxri, N);
    } else {
        auto aux2 = Random::rnd_nums_that_sum(maxci/2, N);
        for (int i = 0; i < N; i++) {
            ris[i] = Random::rnd(1, aux2[i]);
            ris[i] = std::min(ris[i], maxri);
            int p = (i > 0? cis[i-1] + ris[i-1] : 0);
            cis[i] = Random::rnd(p + ris[i], p + aux2[i]);
        }
    }

    Generator::case_in << N << '\n';
    for (auto& it: cis) Generator::case_in << it << ' ';
    Generator::case_in << '\n';
    for (auto& it: ris) Generator::case_in << it << ' ';
    Generator::case_in << '\n';

    return 0;
}