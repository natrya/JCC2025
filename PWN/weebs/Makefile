CC := gcc
UNAME_S := $(shell uname -s)

CFLAGS := -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wall -Wextra
LDFLAGS :=

ifeq ($(UNAME_S),Linux)
  CFLAGS += -fno-PIE -no-pie
  LDFLAGS += -Wl,-z,relro -Wl,-z,now -ldl
endif

SRC_DIR := src
BUILD_DIR := build
BIN := $(BUILD_DIR)/chal

SRCS := $(SRC_DIR)/chal.c

.PHONY: all clean rebuild

all: $(BIN)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BIN): $(SRCS) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf $(BUILD_DIR)

rebuild: clean all


