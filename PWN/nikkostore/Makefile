CC ?= gcc
CFLAGS ?= -O0 -g -Wall -Wextra -Wno-unused-result

SRC := src/store.c
BIN := store

all: $(BIN)

$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC)

debug: CFLAGS := -O0 -g -fsanitize=address,undefined
debug: clean $(BIN)

linux: CFLAGS := -O2 -no-pie -fno-stack-protector
linux: clean $(BIN)

clean:
	rm -f $(BIN)

.PHONY: all debug linux clean

