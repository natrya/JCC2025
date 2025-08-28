#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

void give_flag(){
 /*
    your win function, no need to worry about this
  */
}

void sigsegv_handler(int sig){
  give_flag();
  /*
    your win function, no need to worry about this
  */
}

void setup(){
  /*
    your win function, no need to worry about this
  */

  signal(SIGSEGV, sigsegv_handler);
}

void vuln(){
  char buffer[0x100];
  gets(buffer);
}

int main(){
  setup();
  /*
    your win function, no need to worry about this
  */

  vuln();
  /*
    your win function, no need to worry about this
  */

  return 0;
}