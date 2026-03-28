#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N; cin >> N;
    int64_t zeros = N;
    int64_t parejas = zeros * (zeros-1)/2;
    unordered_map<int, int64_t> bucket;
    for (int i = 0; i < N; i++) {
        int64_t x; cin >> x >> x;
        if (x == 0) {
            cout << parejas << ' ';
            continue;
        }
        parejas -= N - zeros;
        parejas += bucket[x]++;
        zeros--;
        cout << parejas << ' ';
    }
    return 0;
}