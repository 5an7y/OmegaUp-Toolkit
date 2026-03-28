// NOTE: it is recommended to use this even if you don't understand the following code.

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstdint>

using namespace std;

int main() {
    int N;
    cin >> N;

    vector<int> X(N);
    for (int i = 0; i < N; ++i)
        cin >> X[i];

    vector<long long> R(N);
    for (int i = 0; i < N; ++i)
        cin >> R[i];

    long long ans = 0;

    for (int i = 0; i < N; i++) {
        ans += R[i] * 2 * R[i] * 2;
    }

    cout << ans << endl;

    return 0;
}
