#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N; cin >> N;
    int ans = 0;
    for (int i = 1; i <= N; i++) {
        int x; cin >> x;
        ans = __gcd(ans, abs(x - i));
    }
    cout << ans << '\n';

    return 0;
}