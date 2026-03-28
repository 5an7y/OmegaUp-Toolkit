#include <bits/stdc++.h>
using namespace std;

#define maxa 2000001

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N; cin >> N;
    vector<int> nums(N), bucket(maxa);
    for (auto& it : nums) {
        cin >> it;
        bucket[it]++;
    }
    int64_t gcd = 1;
    vector<bool> shieve(maxa);
    //cerr << "Hello" << std::endl;
    for (int64_t i = 2; i < maxa; i++) {
        if (!shieve[i]) {
            shieve[i] = true;
            // Mark no primes
            for (int64_t j = i*i; j < maxa; j+=i) 
                shieve[j] = true;
            int count = 0;
            int64_t num = 1;
            do {
                count = 0;
                num *= i;
                for (int64_t j = num; j < maxa; j+=num) count += bucket[j];
            } while (count >= N-1);
            gcd *= num / i;
        }
    }

    cout << gcd << '\n';

    return 0;
}