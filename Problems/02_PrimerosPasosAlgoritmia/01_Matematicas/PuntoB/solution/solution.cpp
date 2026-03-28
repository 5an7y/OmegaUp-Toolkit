#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int n, k; cin >> n >> k;
    if (n < k) cout << k-n << '\n';
    else cout << 1 - (n % 2 == k % 2) << '\n'; 
    return 0;
}