#include <iostream>
#include <set>
#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);    
    /*
        Use Generator::case_in<< to put elements in case input.
        Use Generator::case_out<< to put elements in case output.
        Use Generator::arguments>> to read the arguments.
    */
    std::string case_type;
    int N, tries;
    Generator::arguments >> case_type >> N >> tries;
    if (case_type == "CUSTOM1") {
        Generator::case_in << 
        "5"
        "..#..#\n"
        ".###..\n"
        ".##...\n"
        "###...\n"
        ".#....\n";
    } else if (case_type == "CUSTOM2") {
        Generator::case_in << 
        "5"
        "..#..#\n"
        ".#####\n"
        ".##..#\n"
        "###...\n"
        ".#....\n";
    } else if (case_type == "RANDOM") {
        auto vec = Random::rnd_unique(0, N * N-1, tries);
        std::set<int> conj(vec.begin(), vec.end());
        Generator::case_in << N << '\n';
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) 
                Generator::case_in << ".#"[conj.count(i * N + j)];
            Generator::case_in << '\n';
        }
    } else {
        auto points = Random::rnd_unique(0, (N-2) * (N-2) - 1, tries);
        for (auto& it : points) {
            int xi = it / (N-2);
            int xj = it % (N-2);
            xi++, xj++;
            it = xi * N + xj;
        }
        std::set<int> conj(points.begin(), points.end());
        char mat[N][N]; 
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                mat[i][j] = '.';

        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) 
                if (conj.count(i * N + j)) {
                    if (mat[i-1][j] == '.' && 
                        mat[i+1][j] == '.' &&
                        mat[i][j+1] == '.' &&
                        mat[i][j-1] == '.')
                    mat[i-1][j] = mat[i+1][j] = mat[i][j+1] = mat[i][j-1] = mat[i][j] = '#';
                }
    
        Generator::case_in << N << '\n';
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++)
                Generator::case_in << mat[i][j];
            Generator::case_in << '\n';
        }
    }

    return 0;
}