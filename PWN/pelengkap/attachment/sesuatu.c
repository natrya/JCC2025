#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void vuln() {
    char buf[256];
    printf("Kirimkan sesuatu kepadaku:");
    read(0, buf, 256);
    ((void(*)())buf)();
}

int main() {
    setbuf(stdout, NULL);
    vuln();
    return 0;
}

