#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N; cin >> N;
    vector<int> vec(N), vec2(N);
    for (auto& it : vec) cin >> it;
    for (auto& it : vec2) cin >> it;
    int s = 0;
    for (int i = 0; i < N; i++)
        s += abs(vec[i] - vec2[i]);
    
    cout << s << '\n';

    return 0;
}