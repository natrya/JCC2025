UNAME_S := $(shell uname -s)
CC ?= clang

SRC := kpop.c
BIN_DIR := bin
BIN := $(BIN_DIR)/kpop

CFLAGS_COMMON := -O0 -g -Wall -Wextra -Wno-format -Wno-format-security

ifeq ($(UNAME_S),Darwin)
CFLAGS := $(CFLAGS_COMMON) -fno-stack-protector -Wl,-no_pie
DEFAULT := mac
else
CFLAGS := $(CFLAGS_COMMON) -fno-stack-protector -fno-PIE -no-pie
DEFAULT := linux
endif

.PHONY: all mac linux clean run serve

all: $(DEFAULT)

mac: $(BIN)

linux: $(BIN)

$(BIN): $(SRC)
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

run: $(BIN)
	./$(BIN)

serve: $(BIN)
	@echo "Starting net service on 127.0.0.1:9001 via socat..."
	socat -T60 TCP-LISTEN:9001,reuseaddr,fork EXEC:./$(BIN),pty,rawer,echo=0

clean:
	rm -rf $(BIN_DIR)
