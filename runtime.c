/* a simple driver for scheme_entry */
#include <stdio.h>

#define EMPTY_LIST 0x2f
#define FIXNUM_MASK 3
#define FIXNUM_TAG 0
#define FIXNUM_SHIFT 2

int main(int argc, char** argv) {
    int val = scheme_entry();
    if ((val & FIXNUM_MASK) == FIXNUM_TAG) {
        printf("%d\n", val >> FIXNUM_SHIFT);
    } else if (val == EMPTY_LIST) {
        printf("()\n");
    }
    return 0;
}
