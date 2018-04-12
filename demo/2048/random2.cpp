#include <bits/stdc++.h>
using namespace std;
typedef long long LL;

int main() {
    int a, b, counter = 0;
    while (1) {
        if (scanf("%d", &a) == EOF) break;
        if (a == 0) break;
        for (int i = 0; i < 16; ++i)
            scanf("%d", &b);
        switch (counter % 2) {
            case 0: cout << "S" << endl; break;
            case 1: cout << "D" << endl; break;
        }
        counter++;
    }
}
