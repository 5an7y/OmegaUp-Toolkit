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
    int N, Y; 
    Generator::arguments >> N >> Y;
    int mini = Y <= 2 ? 1 : 0;
    N = Random::rnd(1, N);
    auto scores = Random::rnd(mini, Y, N);
    std::vector<int> pep(N);
    std::iota(pep.begin(), pep.end(), 1);
    std::random_shuffle(pep.begin(), pep.end());
    for (int i = 0; i < N; i++) 
        Generator::case_in << pep[i] << ' ' << scores[i] << '\n';

    return 0;
}