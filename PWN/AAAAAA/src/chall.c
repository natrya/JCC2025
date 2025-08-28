#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

void give_flag(){
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

  printf("%s%s%s",
  "\nTcih. y, y, y, nih!\n",
  flag,
  "\nsekarang diem y.\n");
}

void sigsegv_handler(int sig){
  give_flag();
  fflush(stdout);
  exit(1);
}

void setup(){
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

  signal(SIGSEGV, sigsegv_handler);
}

void vuln(){
  char buffer[0x100];
  gets(buffer);
}

int main(){
  setup();

  printf("%s%s%s%s",
        "ini udh malem kocak\n",
        "bisa diem ga si lu, gausa rame\n",
        "makasi y\n\n",
        "Input: ");
  fflush(stdout);

  vuln();
  printf("\nhhhhhhhh.......");

  return 0;
}