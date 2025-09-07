#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

char *alamat_printf;

void cetak_banner() {
    printf("    ___     _       _      _     \n");
    printf("   /   |   (_)     (_)    | |    \n");
    printf("  / /| |    _       _   __| |    \n");
    printf(" / ___ |   | |     | | / _` |    \n");
    printf("/_/  |_|   | |     | || (_| |    \n");
    printf("          _/ | _   | | \\__,_|    \n");
    printf("         |__/ (_)  | |           \n");
    printf("                 _/ |            \n");
    printf("                |__/             \n");
    printf("\n");
}

void pencari_printf() {
    char buffer[64];
    puts("Alamat printf berhasil ditemukan di:");
    puts(alamat_printf);
    puts("Eh, kok kamu bisa sampai sini?");
    fflush(stdin);
    gets(buffer);  // vulnerability
    return;
}

void mulai_tantangan() {
    char buffer[64];
    asprintf(&alamat_printf, "%p", printf);

    printf("Selamat datang di pencari aplikasi ajaib!\n");
    printf("Sayangnya, layanan ini masih dalam tahap pengembangan.\n");
    printf("Kami percaya pada Open Source, tapi GitHub jahat,\n");
    printf("jadi kami hosting sendiri kode kami di situs web pribadi.\n");
    printf("Mungkin kamu bisa kirim kontribusi lewat email?\n");
    printf("Saat ini hanya fungsi pencari_printf yang sudah jadi, lokasinya ada di: %p\n", pencari_printf);
    printf("Tapi tenang, kamu belum bisa memanggilnya sebelum semua layanan selesai.\n");

    printf("Kalau mau, kamu bisa kasih kami masukan: \n");
    gets(buffer);  // vulnerability
    return;
}

int main(int argc, char* argv[]) {
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);
    cetak_banner();
    mulai_tantangan();
    fflush(stdout);
    printf("Terima kasih atas masukanmu!\n");
    return 0;
}

