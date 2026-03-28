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
   int p; Generator::arguments >> p;
   int N = Random::rnd(10, 100);
   if (p == 0) {
        Generator::case_in << N << '\n';
        for(int i = 0; i < N; i++) Generator::case_in << 0 << ' ';
        Generator::case_out << 0 << '\n';
   } else if (p == 1) {
    Generator::case_in << N << '\n';
    for(int i = 0; i < N; i++) Generator::case_in << Random::rnd(1, 100) << ' ';
    Generator::case_out << 1 << '\n';
   } else if (p == 2) {
    Generator::case_in << N << '\n';
    for(int i = 0; i < N; i++) Generator::case_in << Random::rnd(0, 10) << ' ';
    Generator::case_out << 2 << '\n';
   } else if (p == 3) {
    Generator::case_in << N << '\n';
    int x = Random::rnd(1, N/2 - 1);
    for(int i = 0; i < x; i++) Generator::case_in << 0 << ' ';
    for(int i = 0; i < N - 2 * x; i++) Generator::case_in << Random::rnd(1, 100) << ' ';
    for(int i = 0; i < x; i++) Generator::case_in << 0 << ' ';
    Generator::case_out << 1 << '\n';
   }

    return 0;
}