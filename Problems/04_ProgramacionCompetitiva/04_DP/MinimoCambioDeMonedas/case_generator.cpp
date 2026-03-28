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
    int N, maxM, maxAi;
    Generator::arguments >> N >> maxAi >> maxM;
    auto vec = Random::rnd_unique(1, maxAi, N);
    int M = Random::rnd(1, maxM);
    bool has_one = false;
    for (auto& it : vec) has_one |= (it == 1);
    if (!has_one) vec[0] = 1;

    Generator::case_in << N << ' ' << M << '\n';
    for (auto& it : vec) 
        Generator::case_in << it << ' ';

    return 0;
}