#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int N; cin >> N;
    char mat[N][N];
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cin >> mat[i][j];
        }
    }

    int counter = 0;

    for (int i = 1; i < N-1; i++) {
        for (int j = 1; j < N-1; j++) {
            if (mat[i][j] == '#' && 
                mat[i-1][j] == '#' &&
                mat[i+1][j] == '#' &&
                mat[i][j-1] == '#' && 
                mat[i][j+1] == '#') {

                mat[i][j] = 
                mat[i-1][j] =              
                mat[i+1][j] =
                mat[i][j-1] = 
                mat[i][j+1] = '.';

                counter++;
            }
        }
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (mat[i][j] == '#') {
                cout << -1;
                return 0;
            }
        }
    }

    cout << counter;

    return 0;
}