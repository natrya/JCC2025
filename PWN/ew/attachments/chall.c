#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FLAGSIZE_MAX 64

void win(){
    char flag[FLAGSIZE_MAX];
    FILE *fd;

    fd = fopen("flag.txt", "r");
    if (fd == NULL){
    printf("%s%s", 
            "flag.txt not found, please create a flag.txt\n",
            "if this happened on remote server please contact admin");
    exit(1);
    }
    fgets(flag, 64, fd);

    printf("\nCongrats! here's your reward: \n");
    printf(flag);
}

void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln(){
    long target = 0x69420;
    char buffer[40];

    printf("Heeiii! Here's a simple challenge\n\n");
    printf("\033[1;36mtarget = \033[1;31m0x%lx\033[1;0m\n\n", target);
    printf("Your task is to change the value of target to \033[1;31m0x1337c0deee\033[1;0m\n");
    printf("Let's see if you're up to the task\n\n");
    printf("payload: ");

    fgets(buffer, 48, stdin);

    printf("\nlet's see...\n");
    sleep(2);
    printf("target = \033[1;31m0x%lx\033[1;0m\n", target);
    
    if(target != 0x1337c0deee){
        printf("feel free to try again!");
        exit(1); 
    } else {
        win();
    }
}

int main(){
    setup();
    vuln();
    return 0;
}