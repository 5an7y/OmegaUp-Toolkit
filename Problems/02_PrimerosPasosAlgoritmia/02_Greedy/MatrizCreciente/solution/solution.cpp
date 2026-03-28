#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N; cin >> N;
    int mat[N+1][N+1];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) cin >> mat[i][j];
    for (int i = 0; i <= N; i++) mat[i][N] = mat[N][i] = 1e8;

    for (int i = N-1; i >= 0; i--) for (int j = N-1; j >= 0; j--) {
        if (mat[i][j] == 0)
            mat[i][j] = min(mat[i+1][j], mat[i][j+1]) - 1;
        if (mat[i][j] == 0 || mat[i][j] >= min(mat[i+1][j], mat[i][j+1])) {
            cout << "NO"; return 0;
        }
    }
    cout << "SI";
    return 0;
}