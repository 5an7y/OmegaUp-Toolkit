#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N; cin >> N;
    int64_t s = 0;
    for (int i = 0; i < N; i++) {
        int x; cin >> x;
        if (x == 0) s++;
        else s += (N-1);
    }

    cout << s << '\n';

    return 0;
}