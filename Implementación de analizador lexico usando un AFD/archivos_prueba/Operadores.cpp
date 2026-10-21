using namespace std;

int main() {
    int a = 10;
    int b = 3;
    int r = 0;
    bool ok = true;

    // Aritmeticos
    r = a + b;
    r = a - b;
    r = a * b;
    r = a / b;
    r = a % b;

    // Asignacion compuesta
    r += 2;
    r -= 2;
    r *= 2;
    r /= 2;
    r %= 3;

    // Incremento y decremento
    a++;
    b--;
    ++a;
    --b;

    // Relacionales
    ok = a == b;
    ok = a != b;
    ok = a < b;
    ok = a <= b;
    ok = a > b;
    ok = a >= b;

    // Logicos
    ok = (a > 0) && (b > 0);
    ok = (a > 0) || (b > 0);
    ok = !ok;

    // Bit a bit
    r = a & b;
    r = a | b;
    r = a ^ b;
    r = ~a;
    r = a << 2;
    r = b >> 1;

    // Ternario
    r = (a > b) ? a : b;

    return 0;
}
