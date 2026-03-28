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
    int N, Q, T; 
    std::string tipo;
    Generator::arguments >> N >> Q >> T >> tipo;
    auto vals = Random::rnd(1, T, N);
    Generator::case_in << N << '\n';
    for(auto& it : vals) Generator::case_in << it << ' ';
    Generator::case_in << '\n';

    if (tipo == "linear") {
        std::vector<int> vec(N);
        std::iota(vec.begin(), vec.end(), 1);
        std::random_shuffle(vec.begin(), vec.end());
        for (int i = 1; i < N; i++)
            Generator::case_in << vec[i-1] << ' ' << vec[i] << '\n';
        Generator::case_in << Q << '\n';
        for (int i = 0; i < Q; i++) {
            int a = Random::rnd(0, 1);
            if (a)
                Generator::case_in << "? " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, N) << '\n';
            else
                Generator::case_in << "+ " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, T) << '\n';
        }
    } else if (tipo == "rand" || tipo == "noupdates") {
        auto t = Random::rnd_tree(N);
        for (auto& [a, b] : t)
            Generator::case_in << a+1 << ' ' << b+1 << '\n';
        Generator::case_in << Q << '\n';
        for (int i = 0; i < Q; i++) {
            int a = Random::rnd(0, 1);
            if (tipo == "noupdates") a = 1;
            if (a)
                Generator::case_in << "? " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, N) << '\n';
            else
                Generator::case_in << "+ " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, T) << '\n';
        }
    } else {
        for (int i = 1; i < N/2; i++) {
            Generator::case_in << i << ' ' << i+1 << '\n';
        }
        Generator::case_in << 1 << ' ' << N/2+1 << '\n';
        for (int i = N/2+1; i < N; i++) {
            Generator::case_in << i << ' ' << i+1 << '\n';
        }

        Generator::case_in << Q << '\n';
        for (int i = 0; i < Q; i++) {
            int a = Random::rnd(0, 1);
            if (tipo == "noupdates") a = 1;
            if (a)
                Generator::case_in << "? " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, N) << '\n';
            else
                Generator::case_in << "+ " << Random::rnd(1, N) 
                                   << " " << Random::rnd(1, T) << '\n';
        }
    }

    return 0;
}