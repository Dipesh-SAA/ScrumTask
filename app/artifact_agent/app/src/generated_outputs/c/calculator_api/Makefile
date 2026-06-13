# Calculator API Makefile

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -I.
LDFLAGS = -lm

TARGET = calculator_api
SRC = src/main.c src/calculator.c src/routes.c src/models.c
OBJ = $(SRC:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJ)

run: $(TARGET)
	./$(TARGET)
