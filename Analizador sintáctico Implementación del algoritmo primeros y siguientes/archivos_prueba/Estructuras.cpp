using namespace std;

struct Punto {
    int x;
    int y;
};

class Cuenta {
private:
    double saldo;
public:
    Cuenta(double inicial) {
        saldo = inicial;
    }
    void depositar(double monto) {
        saldo += monto;
    }
    double obtenerSaldo() {
        return saldo;
    }
};

enum Color { ROJO, VERDE, AZUL };

int main() {
    Punto p;
    p.x = 4;
    p.y = 7;

    Cuenta* cuenta = new Cuenta(100.50);
    cuenta->depositar(25.25);
    cout << cuenta->obtenerSaldo() << endl;
    delete cuenta;

    int numeros[5] = { 1, 2, 3, 4, 5 };
    int suma = 0;
    int i = 0;
    while (i < 5) {
        suma += numeros[i];
        i++;
    }

    int opcion = 2;
    switch (opcion) {
        case 1:
            cout << "Uno" << endl;
            break;
        case 2:
            cout << "Dos" << endl;
            break;
        default:
            cout << "Otro" << endl;
    }

    do {
        suma--;
    } while (suma > 0);

    std::cout << sizeof(int) << endl;

    return 0;
}
