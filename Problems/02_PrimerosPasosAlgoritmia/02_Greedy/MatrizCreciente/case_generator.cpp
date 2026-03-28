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
     int N;
     Generator::arguments >> case_type >> N;
     Generator::case_in << N << '\n';
     int mat[N][N];
     for (int i = 0; i < N; i++)  for (int j = 0; j < N; j++) mat[i][j] = 0;

     if (case_type == "ONLYFIRSTCORNER") {
        mat[0][0] = 100000;
     } else if (case_type == "ONLYLASTCORNERVALID" ) {
        mat[N-1][N-1] = 2 * N - 1;
     } else if (case_type == "ONLYLASTCORNERINVALID" ) {
        mat[N-1][N-1] = 2 * N - 2;
     } else if (case_type == "ONLYCENTERINVALID" ) {
        mat[N/2][N/2] = 2 * (N/2) - 2;
     } else if (case_type == "ONLYRIGHTCORNERVALID" ) {
        mat[N-1][0] = N;
     } else if (case_type == "ONLYLEFTCORNERINVALID" ) {
        mat[0][N-1] = N-1;
     } else if (case_type == "DIAGVALID" ) {
        for (int i = 0; i < N; i++) mat[i][N-1-i] = N;
     } else if (case_type == "DIAGINVALID" ) {
        for (int i = 0; i < N-1; i++) mat[i][N-2-i] = N-2;
     } else {
        auto vec = Random::rnd_unique(1, 100000, N * N);
        sort (vec.begin(), vec.end());
        std::set<std::pair<int, int>> pos;
        pos.insert({N-1, N-1});
        for (int i = 0; i < N * N; i++) {
            int k = Random::rnd(1, (int)pos.size()) - 1;
            auto it = pos.begin();
            std::advance(it, k);
            int xi = it->first;
            int xj = it->second;
            mat[xi][xj] = vec[N * N - 1 - i];
            pos.erase(it);
            // add the one above
            if (xi > 0 && (xj == N-1 || mat[xi - 1][xj + 1] > 0)) {
                pos.insert({xi-1, xj});
            }
            if (xj > 0 && (xi == N-1 || mat[xi + 1][xj - 1] > 0)) {
                pos.insert({xi, xj-1});
            } 
        }

        if (case_type != "FULL") {
            auto disapperi = Random::rnd(0, N-1, 2 * N);
            auto disapperj = Random::rnd(0, N-1, 2 * N);
            for (int i = 0; i < 2 * N; i++) 
                mat[disapperi[i]][disapperj[i]] = 0;
            
            if (case_type == "INVALID") {
                int mat2[N+1][N+1];
                int xi = Random::rnd(0, N-2);
                int xj = Random::rnd(0, N-2);
                mat[xi][xj] = mat[xi+1][xj] = mat[xi][xj+1] = 0; 

                for (int i = 0; i <= N; i++) mat2[N][i] = mat2[i][N] = 100000000;
                for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) mat2[i][j] = mat[i][j];
                if (mat2[N-1][N-1] == 0) mat2[N-1][N-1] = 10000000;
                for (int i = N-1; i >= 0; i--) for (int j = N-1; j >= 0; j--) {
                    if (mat2[i][j] == 0) mat2[i][j] = std::min(mat2[i+1][j], mat2[i][j+1]) - 1;
                }
                mat[xi][xj] = mat2[xi][xj] + 1;
            }
        } 
     }

     for (int i = 0; i < N; i++) {  
        for (int j = 0; j < N; j++) Generator::case_in << mat[i][j] << ' ';
        Generator::case_in << '\n';
     }

    return 0;
}