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
    int N; std::string tipo;
    Generator::arguments >> N >> tipo;
    std::vector<int> vec(N);
    const int MAXAI = 2000000;

    if (tipo == "RAND2") {
        vec = Random::rnd(1, MAXAI, N);    
    } else if (tipo == "RAND") {
        int num = Random::rnd(1, MAXAI);
        std::vector<bool> primes(num+1);
        std::vector<int64_t> primepowers;
        for (int64_t i = 2; i <= num; i++) {
            if (primes[i]) continue;
            for (int64_t j = i * i; j <= num; j+=i)
                primes[j] = true;
            int64_t divi = 1;
            while (num % i == 0) {
                divi *= i;
                num /= i;
            }
            if (divi > 1) primepowers.push_back(divi);
        }
        std::vector<int> pos(N);
        for (int i = 0; i < N; i++) pos[i] = i;
        vec.assign(N, 1);
        for (auto& it : primepowers) {
            std::random_shuffle(pos.begin(), pos.end());
            for (int i = 0; i < N-1; i++)
                vec[pos[i]] *= it;
        }

        for (int i = 0; i < N; i++)
            vec[i] *= Random::rnd(1, std::max(1, MAXAI/vec[i]));
    } else if (tipo == "POW2") {
        const int lo = log2(MAXAI);
        const int a = Random::rnd(0, lo);
        for (int i = 1; i < N; i++)
            vec[i] = 1 << Random::rnd(a, lo);
        
        vec[0] = 1 << Random::rnd(0, lo);
    } else if (tipo == "PRIMES") {
        std::vector<bool> primes(MAXAI+1);
        std::vector<int> p;
        for (int64_t i = 2; i <= MAXAI; i++) {
            if (primes[i]) continue;
            p.push_back(i);
            for (int64_t j = i * i; j <= MAXAI; j+=i)
                primes[j] = true;
        }
        int r = Random::rnd<int>(0, p.size()-1);
        int prime = p[r];
        vec.assign(N-1, prime);
        vec.push_back(p[Random::rnd<int>(0, p.size()-1)]);
    } else {
        std::vector<bool> primes(MAXAI+1);
        std::vector<int> p;
        for (int64_t i = 2; i <= MAXAI; i++) {
            if (primes[i]) continue;
            p.push_back(i);
            for (int64_t j = i * i; j <= MAXAI; j+=i)
                primes[j] = true;
        }
        std::random_shuffle(p.begin(), p.end());
        for (int i = 0; i < N; i++)
            vec[i] = p[i];
    }

    Generator::case_in << vec.size() << '\n';
    for (auto& it: vec) Generator::case_in << it << ' ';

    return 0;
}