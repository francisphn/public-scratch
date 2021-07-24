#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void)
{
    uint64_t count = 0;
    char value;

    do {
        printf("Enter ONE character:\n");
        value = getchar();
        count++;
    } while (value != 'q');

    printf("%ld\n", count);
}
