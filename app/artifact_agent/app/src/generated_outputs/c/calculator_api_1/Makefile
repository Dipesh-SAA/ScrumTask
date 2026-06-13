CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude

SRC = src/main.c src/calculator.c src/handlers.c src/routes.c
OBJ = $(SRC:.c=.o)
TARGET = calculator_api

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all clean