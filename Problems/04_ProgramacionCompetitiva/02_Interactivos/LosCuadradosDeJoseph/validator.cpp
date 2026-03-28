#include <bits/stdc++.h>

int main() {
  // lee "data.in" para obtener la entrada original.
  int64_t N;
  {
    std::ifstream entrada_original("data.in", std::ifstream::in);
    entrada_original >> N;
  }

  // lee entrada estándar para obtener la salida del concursante.
  std::vector<int64_t> ans_constestant(4);
  uint64_t ans;
  for (auto& it : ans_constestant) {
    if (!(std::cin >> it)) {
        std::cerr << "Error leyendo la salida del concursante\n";
        std::cout << 0.0 << '\n';
        return 0;
    }
    if (!(0 <= it && it <= 1e9)) {
        std::cerr << "Numeros invalidos ingresados\n";
        std::cout << 0.0 << '\n';
        return 0;
    }
    ans += it * it;
  }

  if (std::abs<int64_t>(ans - N) >= 10)
    std::cout << 0.0 << std::endl;
  else
    std::cout << (10 - std::abs<int64_t>(ans - N)) / 10 << "." << (10 - std::abs<int64_t>(ans - N)) % 10 << std::endl;
  return 0;
}