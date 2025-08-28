#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>

static void banner(void) {
    puts("\\n\\n");
    puts("=======================");
    puts("  Weebs Arena Online  ");
    puts("=======================");
    puts("Welcome, shinobi! Prove your anime power.\n");
}

static void fastio(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

static void hint_leak(void) {
    // Leak a stable libc address using dlsym so players can compute libc base reliably
    void *libc_puts = dlsym(RTLD_NEXT, "puts");
    printf("[Hint] Senpai's secret jutsu at %p\n", libc_puts);
}

static void chant(void) {
    char buf[256];
    puts("\n[Chant] Shout your battle cry (use your chakra wisely):");
    if (!fgets(buf, sizeof(buf), stdin)) {
        puts("eh?");
        return;
    }
    // Format string vulnerability (intended)
    printf(buf);
    puts("");
}

static void duel(void) {
    volatile char arena[64];
    puts("\n[Duel] Channel your power into the arena:");
    // Classic stack buffer overflow (intended) without using gets (removed in modern libc)
    // Read much more than the buffer size, overflowing into canary and saved return.
    ssize_t n = read(0, (char *)arena, 0x200);
    (void)n;
    puts("Your aura flickers... (did you do enough?)");
}

static void menu(void) {
    char choice[8];
    for (;;) {
        puts("\n=== Menu ===");
        puts("1) Chant battle cry (format power)");
        puts("2) Enter the duel (bof power)");
        puts("3) Exit dojo");
        printf("> ");
        if (!fgets(choice, sizeof(choice), stdin)) {
            break;
        }
        switch (choice[0]) {
            case '1':
                chant();
                break;
            case '2':
                duel();
                break;
            case '3':
                puts("Sayonara, shinobi.");
                return;
            default:
                puts("Huh? That's not an anime move.");
        }
    }
}

int main(void) {
    fastio();
    banner();
    hint_leak();
    menu();
    return 0;
}


