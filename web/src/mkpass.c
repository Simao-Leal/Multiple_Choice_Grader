#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
        int i, max, len = 8;
        char tab[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";

        if (argc < 2) {
                fprintf(stderr, "USAGE: %s max [len [seed]]\n", argv[0]);
                return 1;
        }

				srand(time(0));
        max = atoi(argv[1]);
        if (argc > 2) len = atoi(argv[2]);
        if (argc > 3) srand(atoi(argv[3]));

        if (max < 1 || len < 1) {
                fprintf(stderr, "illegal parameters.\n");
                return 2;
        }

        while (max--) {
                for (i = 0; i < len; i++)
                        printf("%c", tab[rand() % 64]);
                printf("\n");
        }

        return 0;
}
