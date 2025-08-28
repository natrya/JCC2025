#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FLAGSIZE_MAX 64

void win(){
    /*
        your win function, no need to worry about this
    */
}

void setup(){
    /*
        some code, no need to worry about this
    */
}

void vuln(){
    long target = 0x69420;
    char buffer[40];

    /*
        some code, no need to worry about this
    */

    fgets(buffer, 48, stdin);

    /*
        some code, no need to worry about this
    */
    
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