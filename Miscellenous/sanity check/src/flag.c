#include <stdio.h>

int main()
{
    FILE *fp = fopen("flag.txt", "r");
    char flag[100];
    fgets(flag, sizeof(flag), fp);
    printf("%s", flag);
}