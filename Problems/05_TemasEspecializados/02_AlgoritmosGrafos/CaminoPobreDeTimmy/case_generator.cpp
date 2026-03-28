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
    int N, M, Q;
    std::string case_type;
    Generator::arguments >> N >> M >> Q >> case_type;
    std::vector<std::vector<int>> mat(N, std::vector<int>(M));
    if (case_type == "ALLONES") {
        for (auto& vec : mat) for (auto& it : vec) it = 1;
    } else if (case_type == "SOMEROW") {
        int idx = Random::rnd(0, N-1);
        mat[idx] = Random::rnd(0, 1000, M);
    } else {
        for (auto& vec : mat) vec = Random::rnd(0, 1000, M);
    }

    Generator::case_in << N << ' ' << M << '\n';
    for (auto& vec : mat) {
        for (auto& it : vec)
            Generator::case_in << it << ' ';
        Generator::case_in << '\n';
    }
    Generator::case_in << Q << '\n';
    while (Q--) {
        int a1 = Random::rnd(0, N-1),
            a2 = Random::rnd(0, M-1),
            b1 = Random::rnd(0, N-1),
            b2 = Random::rnd(0, M-1);
        Generator::case_in << a1 << ' ' << a2 << ' ' << b1 << ' ' << b2 << '\n';
    }

    return 0;
}