#include <bits/stdc++.h>

#define MOD 10000000000000000-7

int64_t dp[10001][10];

void inicializar(int n) {
  for (int i = 0; i <= n; i++) {
    for (int j = 0; j < 10; j++) {
      dp[i][j] = -1;
    }
  }
  return;
}

int64_t busca(int pos, int num, const std::string& code) {
  
  if (pos == code.size()-1)
    return 1;
  
  if (dp[pos][num] == -1) {
  
    const int next_num = code[pos + 1] - '0';

    int posibilidad = (next_num + num) / 2;
    dp[pos][num] = busca(pos + 1, posibilidad, code);

    if ( (next_num + num) % 2 == 1 ) {
      posibilidad++;
      dp[pos][num] += busca(pos + 1, posibilidad, code);
      dp[pos][num] %= MOD;
    }
  }

  return dp[pos][num];
}

int64_t solve(std::string& code) {
  
  inicializar(code.size());
  int64_t res = 0;
  
  for (int i = 0; i < 10; i++) {
    res += busca(0, i, code);
    res %= MOD;
  }

  return res;
}

int main() {

  std::string fake;
  std::cin >> fake;
  std::cout << solve(fake) << '\n';

  return 0;
}