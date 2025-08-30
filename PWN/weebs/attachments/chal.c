#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

static char secret1[64];
static char secret2[64];
static char secret3[64];
static char secret4[64];
static int unlocked = 0;

static void chomp(char *s) {
    size_t n = strlen(s);
    if (n && (s[n-1] == '\n' || s[n-1] == '\r')) s[n-1] = '\0';
}

static void load_secrets(void) {
    const char *s1 = getenv("SECRET1");
    const char *s2 = getenv("SECRET2");
    const char *s3 = getenv("SECRET3");
    const char *s4 = getenv("SECRET4");
    snprintf(secret1, sizeof(secret1), "%s", s1 ? s1 : "alpha");
    snprintf(secret2, sizeof(secret2), "%s", s2 ? s2 : "beta");
    snprintf(secret3, sizeof(secret3), "%s", s3 ? s3 : "gamma");
    snprintf(secret4, sizeof(secret4), "%s", s4 ? s4 : "delta");
}

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

static void win(void) {
    puts("\\n[Win] Your jutsu overwhelms the opponent!");
    int fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        puts("Flag missing. Summoning shell...");
        system("/bin/sh");
        return;
    }
    char buf[256];
    ssize_t n = read(fd, buf, sizeof(buf) - 1);
    if (n > 0) {
        buf[n] = '\0';
        puts("Flag:");
        puts(buf);
    } else {
        puts("Could not read flag.");
    }
    close(fd);
}

static void chant(void) {
    char buf[256];
    puts("\n[Chant] Speak your Justsu :");
    if (!fgets(buf, sizeof(buf), stdin)) {
        puts("eh?");
        return;
    }
    // Format string vulnerability: attacker controls the format string
    // and can leak the four secrets passed as variadic args
    printf(buf, secret1, secret2, secret3, secret4);
    puts("");
}

static void safe(void) {
    puts("[Safe] You flail around. Nothing happens.");
}

typedef struct {
    char name[32];
    void (*tech)(void);
} Arena;

static Arena arena = { .name = "rookie", .tech = safe };

static void practice(void) {
    puts("\n[Practice] Refine your form:");
    printf("Name your kata: ");
    // Intentionally oversized read to allow overwriting the function pointer
    ssize_t n = read(0, (char *)arena.name, 0x100);
    (void)n;
    printf("Your focus aligns at %p\n", (void*)&arena.tech);
}

static void perform(void) {
    puts("\n[Perform] Time to use your technique!");
    arena.tech();
}

static void open_seal(void) {
    char in[128];
    puts("\n[Seal] Four trials guard the path.");
    printf("Secret #1: ");
    if (!fgets(in, sizeof(in), stdin)) return;
    chomp(in);
    if (strcmp(in, secret1) != 0) { puts("Nope."); return; }
    printf("Secret #2: ");
    if (!fgets(in, sizeof(in), stdin)) return;
    chomp(in);
    if (strcmp(in, secret2) != 0) { puts("Nope."); return; }
    printf("Secret #3: ");
    if (!fgets(in, sizeof(in), stdin)) return;
    chomp(in);
    if (strcmp(in, secret3) != 0) { puts("Nope."); return; }
    printf("Secret #4: ");
    if (!fgets(in, sizeof(in), stdin)) return;
    chomp(in);
    if (strcmp(in, secret4) != 0) { puts("Nope."); return; }
    unlocked = 1;
    puts("The seal opens...");
}

static void execute_cmd(void) {
    if (!unlocked) {
        puts("Not ready. Seek the secrets first.");
        return;
    }
    char cmd[256];
    puts("\n[Jutsu] What technique will you unleash?");
    if (!fgets(cmd, sizeof(cmd), stdin)) return;
    chomp(cmd);
    system(cmd);
}

static void menu(void) {
    char choice[8];
    for (;;) {
        puts("\n=== Menu ===");
        puts("1) Chant");
        puts("2) Open the seal");
        puts("3) Execute technique");
        puts("4) Exit dojo");
        printf("> ");
        if (!fgets(choice, sizeof(choice), stdin)) {
            break;
        }
        switch (choice[0]) {
            case '1':
                chant();
                break;
            case '2':
                open_seal();
                break;
            case '3':
                execute_cmd();
                break;
            case '4':
                puts("Sayonara, shinobi.");
                return;
            default:
                puts("Huh? That's not an anime move.");
        }
    }
}

int main(void) {
    fastio();
    load_secrets();
    banner();
    menu();
    return 0;
}


