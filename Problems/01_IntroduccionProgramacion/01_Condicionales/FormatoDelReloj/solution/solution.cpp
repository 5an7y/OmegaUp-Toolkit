#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    int a; cin >> a;
    string b; cin >> b;

    if (a >= 12) {
        a -= 12;
        if (a == 0) cout << 12;
        else if (a < 10) cout << 0 << a;
        else cout << a;

        cout << b << " PM\n";
    } else {
        if (a == 0) cout << 12;
        else if (a < 10) cout << 0 << a;
        else cout << a;

        cout << b << " AM\n";
    }

    return 0;
}