#include <stdio.h>
#include <stdlib.h>

int main() {
    int check = system("python3 --version > /dev/null 2>&1");

    if (check == 0) {
        printf("YES\n");
        return 0;
    } else {
        printf("NO\n");
        return 1;
    }
}