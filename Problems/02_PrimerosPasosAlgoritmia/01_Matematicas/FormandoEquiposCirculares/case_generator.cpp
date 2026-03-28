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
    
    int teams, L, N;
    Generator::arguments >> teams >> L;

    if (teams != 1) N = Random::rnd(teams, 400);
    else N = 2;

    auto vec = Random::rnd(0, teams-1, N-1);
    Generator::case_in << N << ' ' << L << '\n';

    int act = 0;
    auto other = Random::rnd_unique(0, L-1, teams);
    for (auto& it : vec) {
        int dest = other[it];
        if (act < dest) Generator::case_in << dest - act << ' ';
        else Generator::case_in << L - (act - dest) << ' ';
    }

    return 0;
}