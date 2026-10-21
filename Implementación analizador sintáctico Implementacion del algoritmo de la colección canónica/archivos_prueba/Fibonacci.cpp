using namespace std;

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int limite = 10;

    for (int i = 0; i < limite; i++) {
        cout << fibonacci(i) << " ";
    }
    cout << endl;

    return 0;
}
