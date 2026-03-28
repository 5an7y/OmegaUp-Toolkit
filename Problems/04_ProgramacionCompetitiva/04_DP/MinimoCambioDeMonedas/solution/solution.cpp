#include <bits/stdc++.h>
using namespace std;
int N, M;
vector<int> DP, coins;

int main() {
    ios_base::sync_with_stdio(0); cin.tie(0);
    cin >> N >> M;
    DP.resize(M+1, M+1);
    coins.resize(N);
    for (auto& it : coins) cin >> it;

    DP[0] = 0;
    for (int i = 1; i <= M; i++)
        for (auto& it : coins) {
            if (i-it < 0) continue;
            DP[i] = min(DP[i-it]+1, DP[i]);
        }
    cout << DP[M] << '\n';
    return 0;
}