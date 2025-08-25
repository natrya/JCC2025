#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <signal.h>

#define MAX_FLAG_LEN 256
#define MAX_QUERY_LEN 128

typedef struct {
	const char *name;
	const char *group;
	const char *position;
	const char *birthday;
	const char *nationality;
} Member;

static char g_flag[MAX_FLAG_LEN];
static char g_seg1[MAX_FLAG_LEN];
static char g_seg2[MAX_FLAG_LEN];
static char g_seg3[MAX_FLAG_LEN];

static void trim_newline(char *s) {
	if (!s) return;
	size_t n = strlen(s);
	if (n && (s[n-1] == '\n' || s[n-1] == '\r')) s[n-1] = '\0';
}

static int caseicmp(const char *a, const char *b) {
	for (; *a && *b; a++, b++) {
		int ca = tolower((unsigned char)*a);
		int cb = tolower((unsigned char)*b);
		if (ca != cb) return ca - cb;
	}
	return tolower((unsigned char)*a) - tolower((unsigned char)*b);
}

static void load_flag_into_memory(void) {
	FILE *f = fopen("flag.txt", "r");
	if (!f) {
		perror("[error] open flag.txt");
		fprintf(stderr, "Make sure flag.txt exists next to the binary.\n");
		exit(1);
	}
	size_t n = fread(g_flag, 1, MAX_FLAG_LEN - 1, f);
	g_flag[n] = '\0';
	fclose(f);

	/* Split the flag into three segments to increase exploitation effort */
	size_t n1 = n / 3;
	size_t n2 = (n - n1) / 2;
	size_t n3 = n - n1 - n2;
	memcpy(g_seg1, g_flag, n1);
	g_seg1[n1] = '\0';
	memcpy(g_seg2, g_flag + n1, n2);
	g_seg2[n2] = '\0';
	memcpy(g_seg3, g_flag + n1 + n2, n3);
	g_seg3[n3] = '\0';
}

static void cat_flag_sneaky(void) {
	/* Perform a cat of flag.txt at startup but do not forward output to user. */
	FILE *p = popen("cat flag.txt", "r");
	if (p) {
		char sink[256];
		while (fgets(sink, sizeof(sink), p)) {
			/* intentionally discard */
		}
		pclose(p);
	}
}

static void disable_stdio_buffering(void) {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

static Member members[] = {
	/* TWICE */
	{"Nayeon",   "TWICE", "Lead Vocalist", "1995-09-22", "Korean"},
	{"Jeongyeon","TWICE", "Lead Vocalist", "1996-11-01", "Korean"},
	{"Momo",     "TWICE", "Main Dancer, Rapper", "1996-11-09", "Japanese"},
	{"Sana",     "TWICE", "Vocalist", "1996-12-29", "Japanese"},
	{"Jihyo",    "TWICE", "Leader, Main Vocalist", "1997-02-01", "Korean"},
	{"Mina",     "TWICE", "Main Dancer, Vocalist", "1997-03-24", "Japanese"},
	{"Dahyun",   "TWICE", "Rapper, Vocalist", "1998-05-28", "Korean"},
	{"Chaeyoung","TWICE", "Rapper, Vocalist", "1999-04-23", "Korean"},
	{"Tzuyu",    "TWICE", "Lead Dancer, Vocalist", "1999-06-14", "Taiwanese"},
	/* IVE */
	{"Yujin",    "IVE",   "Leader, Vocalist", "2003-09-01", "Korean"},
	{"Gaeul",    "IVE",   "Rapper, Dancer", "2002-09-24", "Korean"},
	{"Rei",      "IVE",   "Rapper, Vocalist", "2004-02-03", "Japanese"},
	{"Wonyoung", "IVE",   "Vocalist, Dancer", "2004-08-31", "Korean"},
	{"Liz",      "IVE",   "Vocalist", "2004-11-21", "Korean"},
	{"Leeseo",   "IVE",   "Vocalist, Maknae", "2007-02-21", "Korean"},
};

static void list_all(void) {
	puts("==== KPOP DATABASE (TWICE & IVE) ====");
	for (size_t i = 0; i < sizeof(members)/sizeof(members[0]); i++) {
		printf("[%2zu] %-9s | Group: %-5s | %-30s | DOB: %-10s | %s\n",
			i+1,
			members[i].name,
			members[i].group,
			members[i].position,
			members[i].birthday,
			members[i].nationality);
	}
}

static int find_by_name(const char *q) {
	for (size_t i = 0; i < sizeof(members)/sizeof(members[0]); i++) {
		if (caseicmp(members[i].name, q) == 0) return (int)i;
	}
	return -1;
}

static void handle_search(void) {
	char query[MAX_QUERY_LEN];
	printf("Enter member name: ");
	if (!fgets(query, sizeof(query), stdin)) return;
	trim_newline(query);

	int idx = find_by_name(query);
	if (idx >= 0) {
		Member *m = &members[idx];
		puts("-- RESULT --");
		printf("Name   : %s\n", m->name);
		printf("Group  : %s\n", m->group);
		printf("Role   : %s\n", m->position);
		printf("DOB    : %s\n", m->birthday);
		printf("Nation : %s\n", m->nationality);
	} else {
		puts("Not found.");
	}

	/* Vulnerable echo: user controls format string. Pass scattered fragments at sparse positions. */
	printf("Echo: ");
	printf(
		query,
		"NOFLAG",             /* %1$s */
		"KEEP TRYING",        /* %2$s */
		"NOT HERE",           /* %3$s */
		g_seg2,               /* %4$s */
		"ALMOST",             /* %5$s */
		"NEARLY",             /* %6$s */
		g_seg1,               /* %7$s */
		"MAYBE",              /* %8$s */
		g_seg3                /* %9$s */
	);
	printf("\n");
}

static void menu_loop(void) {
	char buf[8];
	while (1) {
		puts("");
		puts("1) List all members");
		puts("2) Search member");
		puts("3) Exit");
		printf("> ");
		if (!fgets(buf, sizeof(buf), stdin)) break;
		int choice = atoi(buf);
		switch (choice) {
			case 1: list_all(); break;
			case 2: handle_search(); break;
			case 3: puts("Bye."); return;
			default: puts("Invalid choice.");
		}
	}
}

int main(void) {
	disable_stdio_buffering();
	alarm(120);
	load_flag_into_memory();
	cat_flag_sneaky();
	puts("Welcome to KPOP DATABASE (TWICE & IVE)");
	menu_loop();
	return 0;
}
