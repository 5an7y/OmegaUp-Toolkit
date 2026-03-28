#include <iostream>
#include <algorithm>
#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    int op;
    Generator::arguments >> op;
    int N = Random::rnd(3, 30);
    std::vector<int> vec;
    if (op == -1) {
        vec = Random::rnd(1, 10000, N);
    } else {
        vec = Random::rnd_unique(1, 1 << 10, N);
        std::sort(vec.begin(), vec.end());
        for (auto & it : vec) {
            while (it < 1e9 / 2) {
                if (Random::rnd(0, 6)) {
                    it *= 2;
                    if (Random::rnd(0, 1)) it++;
                } else {
                    break;
                }
            }
        }
    }

    Generator::case_in << N << '\n';
    for (auto& it : vec)
        Generator::case_in << it << ' ';
    
    return 0;
}