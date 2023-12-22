#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{

  FILE *in1, *in2 = stdin, *out = stdout;
  char buf[BUFSIZ];

  switch (argc) {
    case 4: if ((out = fopen(argv[3], "w")) == 0) {
                perror(argv[3]);
                exit(1);
            }
    case 3: if ((in2 = fopen(argv[2], "r")) == 0) {
                perror(argv[2]);
                exit(1);
            }
    case 2: if ((in1 = fopen(argv[1], "r")) == 0) {
                perror(argv[1]);
                exit(1);
            }
            break;
    default: fprintf(stderr, "USAGE: %s file1 [file2 [outfile]]\n", argv[0]);
            break;
  }

  while (fgets(buf, BUFSIZ-1, in1) != 0) {
    buf[strlen(buf)-1] = 0; /* remove trailing \n */
    fprintf(out, "%s ", buf);
    if (fgets(buf, BUFSIZ-1, in2) != 0)
      fprintf(out, "%s", buf);
    else
      fprintf(out, "\n");
  }
  while (fgets(buf, BUFSIZ-1, in2) != 0) /* flush remaining lines in file2 */
    fprintf(out, "%s", buf);


  return 0;
}
