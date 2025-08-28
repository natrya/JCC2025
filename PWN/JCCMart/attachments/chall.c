#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

void win(){
  /*
    you win function, no need to worry about the code
  */
}

void setup(){
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

void menu(){
  puts("apa yang mau kamu beli hari ini?");
  puts("(1) kopi susu Rp.99");
  puts("(2) circle Rp.1");
  puts("(3) joki skripsi Rp.666");
}

int main(){
  setup();
  int moneyyyy = 1337;
  long c = 0;
  long n = 0;

  puts("selamat datang di Warung JCCMart\n");
  while(1){
    if(moneyyyy <= 0 || moneyyyy > 1337){
      puts("lho kok aneh ya saldo nya?");
    }

    printf("saldo kamu: Rp.%d\n", moneyyyy);
    menu();
    scanf("%d", &c);

    switch(c){
        case 1:
          puts("mau beli berapa?");
          scanf("%d", &n);
          moneyyyy -= n * 99;
          puts("berhasil membeli kopi susu <3\n");
          break;
        case 2:
          puts("mau beli berapa?");
          scanf("%d", &n);
          moneyyyy -= n * 1;
          puts("berhasil membeli circle \n");
          break;
        case 3:
          puts("mau beli berapa?");
          scanf("%d", &n);
          moneyyyy -= n * 666;
          puts("berhasil membeli joki skripsi\n");
          break;
        case 1000:
          if(moneyyyy <= 999999999){
            puts("mau flag? harus kaya dlu broh\n");
          } else{
            win();
            exit(1);
          }
          break;
        default:
          puts("klo milih yang benar rek\n");
      }
  
      c = 0;
      n = 0;
    }
  
    return 0;
  }