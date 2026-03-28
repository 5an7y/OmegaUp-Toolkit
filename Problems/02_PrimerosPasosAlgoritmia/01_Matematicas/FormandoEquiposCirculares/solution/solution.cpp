#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N, L; cin >> N >> L;
    int act = 0;
    set<int> circ;
    circ.insert(0);
    for (int i = 0; i < N-1; i++) {
        int x; cin >> x;
        act = (act + x) % L;
        circ.insert(act);
    }
    cout << circ.size();

    return 0;
}