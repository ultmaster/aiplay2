#include <bits/stdc++.h>
#include <fcntl.h>
using namespace std;

int is_valid_fd(int fd)
{
    return fcntl(fd, F_GETFL) != -1 || errno != EBADF;
}

int main(int argc, char* argv[]) {
    printf("-1\n");
    fflush(stdout);
    printf("%d\n", is_valid_fd(atoi(argv[1])));
    printf("%d\n", is_valid_fd(atoi(argv[2])));

    FILE* reader = fdopen(atoi(argv[1]), "r");
    FILE* writer = fdopen(atoi(argv[2]), "w");

    for (int i = 0; i < 10; ++i) {
        fprintf(writer, "%d %d\n", i, i + 1);
        fflush(writer);
        int a; fscanf(reader, "%d", &a);
        printf("%d %d\n", i, i + 1);
        printf("%d\n", a);
        fflush(stdout);
    }
    fclose(reader);
    fclose(writer);
    return 0;
}