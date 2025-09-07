#include <stdio.h>
#include <stdlib.h>

void win() {
    FILE *f = fopen("/opt/challs/bin/flag_ret2win.txt","r");
    if (!f){puts("flag missing"); exit(1);}
    char buf[128];
    fgets(buf,128,f);
    puts(buf);
    fclose(f);
}

void vuln() {
    char buf[32];
    printf("Enter input:");
    gets(buf);
}

int main() {
    setbuf(stdout, NULL);
    vuln();
    return 0;
}

