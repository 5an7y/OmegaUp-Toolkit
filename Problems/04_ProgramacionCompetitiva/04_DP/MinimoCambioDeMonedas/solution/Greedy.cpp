#include <bits/stdc++.h>
using namespace std;

int N, M;
vector<int> coins;

int main() {
    ios_base::sync_with_stdio(0); cin.tie(0);
    cin >> N >> M;

    coins.resize(N);
    for (auto& it : coins) cin >> it;
    sort(coins.rbegin(), coins.rend());
    int ans = 0;
    for (auto& it : coins) {
        if (M >= it) {
            ans += M/it;
            M %= it;
        }
    }

    cout << ans;
    return 0;
}