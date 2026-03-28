#include <bits/stdc++.h>
#include "Sofiacienta.h"
using namespace std;

int N, T, ans, anterior, act_day;
bool solved;

char MandarCabellero(int x) {
	act_day++;
	if (x < 0 || x > N) {
		cout << 0.0 << '\n';
		exit(0);
	}
	
	if (act_day > T) {
		cout << 0.0 << '\n';
		exit(0);
	}

	if (act_day == 1) {
		anterior = x;
		cerr << "[Noche] Como es el primer dia no ha llegado ningun cabellero de vuelta" << std::endl;
		return 'x'; 
	}

	char ret = (anterior < ans)? '-' : (anterior > ans) ? '+' : 'S';
	anterior = x;
	cerr << "[Noche] Llego cabellero del dia " << act_day-1;
	if (ret == '-') {
		cerr << " pero la talla fue muy chica" << std::endl;
	} else if (ret == '+') {
		cerr << " pero la talla fue muy grande" << std::endl;
	} else {
		solved = true;
		cerr << " y llego justamente con la talla correcta!" << std::endl;
	}
	return ret;
}

int main(int argc, char* argv[]) {
	cin >> N >> T >> ans;

	act_day = 0; solved = false;
	EncontrarZapatillas(N);
	
	if (solved) {
		if (N == 1000000000) {
			if (act_day <= 44)
				cout << 1.0 << '\n';
			else
				cout << fixed << setprecision(4) << ceil((double) 2250000.0 / (double)(act_day*act_day*act_day)) / (double) 26.0 << '\n';
		} else {
			cout << 1.0 << '\n';
		}
	} else {
		cout << 0.0 << '\n';
	}
	return 0;
}
