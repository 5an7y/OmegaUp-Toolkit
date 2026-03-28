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
    int N;
    Generator::arguments >> N;
    if (N == -1) {
        int sz = Random::rnd(1, 10000);
        for (int i = 0; i < sz; i++) Generator::case_in << 0;
        return 0;
    }
    auto vec = Random::rnd(0, 9, N);
    for (auto& it : vec) Generator::case_in << it;
    return 0;
}