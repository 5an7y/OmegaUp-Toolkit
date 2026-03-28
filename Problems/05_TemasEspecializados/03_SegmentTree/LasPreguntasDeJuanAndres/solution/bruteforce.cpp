#include <bits/stdc++.h>
using namespace std;

vector<int> vec;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N; cin >> N;
    vec.resize(N);
    for (auto& it : vec) cin >> it;
    
    int Q; cin >> Q; 
    while (Q--) {
        int a, b, c; cin >> a >> b >> c;
        if (a == 1) {
            b--, c--;
            int maxi = 0;
            for (int i = b; i <= c; i++) maxi = max(maxi, vec[i]);
            cout << maxi << '\n';
        } else {
            vec[b-1] = c; 
        }
    }
    return 0;
}