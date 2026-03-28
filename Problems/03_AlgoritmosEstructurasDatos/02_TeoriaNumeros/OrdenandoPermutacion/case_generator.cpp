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
    int N, K; Generator::arguments >> N >> K;
    std::vector<int> vec(N);
    for (int i = 0; i < N; i++) vec[i] = i + 1;
    auto q = Random::rnd(0, N-K-1, 99);
    for (auto& it: q) std::swap(vec[it], vec[it + K]);

    Generator::case_in << N << '\n';
    for (auto& it : vec) Generator::case_in << it << ' ';

    return 0;
}