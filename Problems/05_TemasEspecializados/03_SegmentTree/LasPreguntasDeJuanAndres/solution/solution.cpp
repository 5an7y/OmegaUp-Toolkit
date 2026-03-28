#include <bits/stdc++.h>
using namespace std;

vector<int> st, vec;

int stbuid(int node, int l, int r) {
    if (l == r) return st[node] = vec[l];
    int m = (l + r) / 2;
    return st[node] = max(
        stbuid(node * 2, l, m), 
        stbuid(node * 2 + 1, m + 1, r)
    );
}

int stqr(int node, int l, int r, int ll, int rr) {
    if (ll <= l && r <= rr) return st[node];
    if (r < ll || rr < l) return 0;
    int m = (l + r)/2;
    return max(
        stqr(node * 2, l, m, ll, rr),
        stqr(node * 2 + 1, m+1, r, ll, rr)
    );
}

int update(int node, int l, int r, int pos, int k) {
    if (pos < l || r < pos) return st[node];
    if (l == r) return st[node] = k;
    int m = (l + r) / 2;
    return st[node] = max(
        update(node * 2, l, m, pos, k),
        update(node * 2 + 1, m+1, r, pos, k)
    );
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int N; cin >> N;
    vec.resize(N);
    for (auto& it : vec) cin >> it;
    st.resize(4 * N);
    stbuid(1, 0, N-1);
    int Q; cin >> Q; 
    while (Q--) {
        int a, b, c; cin >> a >> b >> c;
        if (a == 1) {
            b--, c--;
            cout << stqr(1, 0, N-1, b, c) << '\n';
        } else {
            update(1, 0, N-1, b-1, c);
        }
    }
    return 0;
}