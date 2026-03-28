#include <iostream>
#include <string>

#include "Generator.hpp"
#include "Random.hpp"
#include "Constants.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    int64_t N, K; 
    std::string aux, s;
    Generator::arguments >> N >> aux;
    N = Random::rnd<int64_t>(1, N);
    auto aux2 = Random::rnd<int>(0, Constants::lowercaseEnglishAlphabet.size()-1, N);
    if (aux == "ab")
        for (auto& it : aux2) it %= 2;
    if (aux == "sorted")
        std::sort(aux2.begin(), aux2.end());
    
    for (auto& it : aux2)
        s += Constants::lowercaseEnglishAlphabet[it];
    
    K = Random::rnd<int64_t>(1, N * (N+1) / 2);
    if (aux == "instring")
        K = Random::rnd<int64_t>(1, N);
    if (aux == "two_versions")
        K = Random::rnd<int64_t>(1, 2 * N - 1);
    
    Generator::case_in << s << '\n' << K;
    return 0;
}