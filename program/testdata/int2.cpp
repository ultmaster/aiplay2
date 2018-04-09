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
    printf("%d %d %d %d\n", is_valid_fd(atoi(argv[1])),
                            is_valid_fd(atoi(argv[2])),
                            is_valid_fd(atoi(argv[3])),
                            is_valid_fd(atoi(argv[4])));
    fflush(stdout);

    FILE* reader1 = fdopen(atoi(argv[1]), "r");
    FILE* writer1 = fdopen(atoi(argv[2]), "w");
    FILE* reader2 = fdopen(atoi(argv[3]), "r");
    FILE* writer2 = fdopen(atoi(argv[4]), "w");

    for (int i = 0; i < 10; ++i) {
        fprintf(writer1, "%d\n", i);
        fflush(writer1);
        int a; fscanf(reader1, "%d", &a);
        printf("reader1: %d\n", a);
        fflush(stdout);

        fprintf(writer2, "%d\n", i + 100);
        fflush(writer2);
        fscanf(reader2, "%d", &a);
        printf("reader2: %d\n", a);

        fflush(stdout);
    }
    fclose(reader1);
    fclose(writer1);
    fclose(reader2);
    fclose(writer2);

    return 0;
}