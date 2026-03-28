// NOTE: it is recommended to use this even if you don't understand the following code.

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstdint>

using namespace std;

int main() {
    int N;
    cin >> N;

    vector<int> X(N);
    for (int i = 0; i < N; ++i)
        cin >> X[i];

    vector<int> R(N);
    for (int i = 0; i < N; ++i)
        cin >> R[i];

    long long ans = 0;


    vector<pair<int64_t, int64_t>> parejas(N);
    for (int i = 0; i < N; i++) 
        parejas[i] = {X[i]-R[i], R[i]};
    
    sort(parejas.begin(), parejas.end());
    priority_queue<pair<int64_t, int64_t>> pq;
    int64_t last;

    for (int64_t i = 0; i < N; i++) {
        int64_t act = parejas[i].first;
        while (!(pq.empty()) && pq.top().second <= act) {
            if (pq.top().second > last) {
                ans += (pq.top().first*2) * (pq.top().second - last);
                last = pq.top().second;
            }
            pq.pop();
        }
        if (!pq.empty())
            ans += (pq.top().first*2) * (act - last);
        last = act;
        pq.push({parejas[i].second, parejas[i].first + 2 * parejas[i].second});
    }

    while (!pq.empty()) {
        if (pq.top().second > last) {
            ans += (pq.top().first*2) * (pq.top().second - last);
            last = pq.top().second;
        }
        pq.pop();
    }

    cout << ans << endl;

    return 0;
}
