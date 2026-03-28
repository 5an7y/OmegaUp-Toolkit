#include <bits/stdc++.h>
#include "Sofiacienta.h"
using namespace std;

int N, T, ans, anterior, act_day;
bool solved;

char MandarCabellero(int x) {
	act_day++;
	if (x < 0 || x > N) {
		cerr << "Realizaste una pregunta invalida: " << x << std::endl;
		cout << 0.0 << '\n';
		exit(0);
	}
	cerr << std::endl;
	cerr << "[Dia " + to_string(act_day) +"] Mandaste al caballero en busqueda de la talla " + to_string(x) + "\n";
	if (act_day > T) {
		cerr << "Te pasaste del limite de tiempo\n";
		cout << 0.0 << '\n';
		exit(0);
	}

	if (act_day == 1) {
		anterior = x;
		cerr << "[Noche " + to_string(act_day) + "] Como es el primer dia no ha llegado ningun cabellero de vuelta" << std::endl;
		return 'x'; 
	}

	char ret = (anterior < ans)? '-' : (anterior > ans) ? '+' : 'S';
	anterior = x;
	cerr << "[Noche " + to_string(act_day) + "] Llego cabellero del dia " << act_day-1;
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
		cerr << "Felicidades encontraste la zapatilla antes del evento! :)" << std::endl;
		cout << 1.0 << '\n';
	} else {
		cerr << "No pudiste encontrar la zapatilla :(" << std::endl;
		cout << 0.0 << '\n';
	}
	return 0;
}
