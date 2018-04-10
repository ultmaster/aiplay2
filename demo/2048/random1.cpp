#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

int main() {
    int a, b, counter = 0;
    while (1) {
        for (int i = 0; i < 16; ++i)
            scanf("%d", &b);
        if (scanf("%d", &a) == EOF) break;
        if (a == 0) break;
        switch (counter % 4) {
            case 0: cout << "W" << endl; break;
            case 1: cout << "A" << endl; break;
            case 2: cout << "S" << endl; break;
            case 3: cout << "D" << endl; break;
        }
        counter++;
    }
}
