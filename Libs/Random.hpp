#pragma once

#include <numeric>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include "Background.hpp"
#include "Constants.hpp"

namespace Random {

    inline std::mt19937 rng(std::random_device{}());

    // Generates a random number between [a, b]. (inclusive)
    template <typename T>
    T rnd(T a, T b) {
        std::uniform_int_distribution<T> distrib(a, b);
        return distrib(rng);
    }

    // Generates a random vector filled with numbers between [a, b].
    template <typename T>
    std::vector<T> rnd(T a, T b, std::size_t sz) {
        std::uniform_int_distribution<T> distrib(a, b);

        std::vector<T> vec(sz);
        for (auto& el : vec)
            el = distrib(rng);
        return vec;
    }

    // Generates a random vector filled with UNIQUE numbers between [a, b].
    template <typename T>
    std::vector<T> rnd_unique(T a, T b, std::size_t sz) {
        std::vector<T> vec(sz);
        if (a > b) {
            throw std::invalid_argument("In rnd_unique(a, b) a should be less or equal than b.");
        }
        uint64_t K = b - a + 1;
        Background::ST_checker<uint64_t> st(0, K-1);

        for (int i = 0; i < sz; i++, K--) {
            auto k = rnd<uint64_t>(1, K);
            vec[i] = st.pop_k(k) + a;
        }
        
        return vec;
    }

    // Generates a random pair of numbers between [a, b].
    template <typename T>
    std::pair<T, T> rnd_pair(T a, T b) {
        std::uniform_int_distribution<T> distrib(a, b);
        T a1, a2;
        a1 = distrib(rng);
        a2 = distrib(rng);
        if (a1 > a2) std::swap(a1, a2);
        return {a1, a2};
    }

    // Generates a vector filled with random pair of numbers between [a, b].
    template <typename T>
    std::vector<std::pair<T, T>> rnd_pair(T a, T b, std::size_t sz) {
        std::uniform_int_distribution<T> distrib(a, b);
        std::vector<std::pair<T, T>> vec(sz);

        for (auto& [a1, a2] : vec) {
            a1 = distrib(rng);
            a2 = distrib(rng);
            if (a1 > a2) std::swap(a1, a2);
        }
        return vec;
    }

    // Generates a random string of length `len` using characters from `charset`.
    std::string rnd_string(std::size_t len, const std::string& charset = Constants::lowercaseEnglishAlphabet) {
        if (charset.empty())
            throw std::invalid_argument("In rnd_string: charset cannot be empty.");
        std::uniform_int_distribution<std::size_t> distrib(0, charset.size() - 1);
        std::string result(len, ' ');
        for (auto& c : result)
            c = charset[distrib(rng)];
        return result;
    }

    // Generates a random permutation of [base, base+n).
    std::vector<int> rnd_permutation(int n, int base = 0) {
        std::vector<int> perm(n);
        std::iota(perm.begin(), perm.end(), base);
        std::shuffle(perm.begin(), perm.end(), rng);
        return perm;
    }

    // Generates a vector with random numbers, such that the sum of all numbers equals SUM. If allow_zero flag is enable, zeros are allowed.
    template <typename T>
    std::vector<T> rnd_nums_that_sum(T sum, std::size_t sz, bool allow_zero = false) {
        if (!allow_zero && (T)sz > sum)
            throw std::invalid_argument("In rnd_nums_that_sum: cannot generate " + std::to_string(sz) + " positive numbers that sum to " + std::to_string(sum) + ".");
        std::vector<T> uniqueRandom;
        if (allow_zero) uniqueRandom = rnd(0, sum, sz);
        else uniqueRandom = rnd_unique(0, sum-1, sz);
        
        std::sort(uniqueRandom.begin(), uniqueRandom.end());
        uniqueRandom.push_back(sum);
        std::vector<T> vec(sz);
        for (int i = 1; i <= sz; i++)
            vec[i - 1] = uniqueRandom[i] - uniqueRandom[i - 1];
        
        return vec;
    }

    // Generates a random tree, the return vector are the edges of the tree.
    std::vector<std::pair<int, int>> rnd_tree(int N) {
        if(N == 1) return {};

        std::vector<int> parents(N);
        for (int i = 1; i < N; i++) 
            parents[i] = Random::rnd(0, i-1);
        
        std::vector<int> remapping(N);
        std::iota(remapping.begin(), remapping.end(), 0);
        std::shuffle(remapping.begin(), remapping.end(), rng);

        std::vector<std::pair<int, int>> vec(N-1);
        for (int i = 1; i < N; i++) {
            parents[i] = remapping[parents[i]];
            vec[i-1] = ( 
                rnd(0, 1) ? std::make_pair(remapping[i], parents[i]) : std::make_pair(parents[i], remapping[i])
            );
        }
        
        return vec;
    }

    // Generates a random forest, the return vector are the edges of the forest. N is the numbers of nodes and trees the number of trees in the forest.
    std::vector<std::pair<int, int>> rnd_forest(int N, int trees) {
        if (N < trees) {
            throw std::invalid_argument("The number of nodes should be at least equal to the number of forest.");
        }
        auto tree_szs = rnd_nums_that_sum(N, trees);
        auto permutation = rnd_unique(0, N-1, N);
        std::vector<std::pair<int, int>> edges;
        int shifted = 0;

        for (int i = 0; i < trees; i++) { 
            int sz = tree_szs[i];
            auto subtree = rnd_tree(sz);
            for (auto [a, b] : subtree) edges.push_back({permutation[a + shifted], permutation[b + shifted]});
            shifted += sz;
        }
        
        return edges;
    }
}