#include <iostream>
#include <numeric>

#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    int N, T; 
    Generator::arguments >> N >> T;
    if (N == 7) {
        int x; Generator::arguments >> x;
        Generator::case_in << N << " " << T << " " << x;
    } else {
        Generator::case_in << N << " " << T << " " << Random::rnd(1, N);
    }
    return 0;
}