/* a simple driver for scheme_entry */
#include <stdio.h>

#define EMPTY_LIST 0x2f

#define FIXNUM_MASK 3
#define FIXNUM_TAG 0
#define FIXNUM_SHIFT 2

#define CHAR_SHIFT 8
#define CHAR_MASK 0xff
#define CHAR_TAG 0x0f

#define BOOL_SHIFT 7
#define BOOL_MASK 0x7f
#define BOOL_TAG 0x1f

int main(int argc, char** argv) {
    int val = scheme_entry();
    if ((val & FIXNUM_MASK) == FIXNUM_TAG) {
        printf("%d\n", val >> FIXNUM_SHIFT);
    }
    else if ((val & CHAR_MASK) == CHAR_TAG) {
        int c = val >> CHAR_SHIFT;
        switch (c) {
        case '\t': printf("#\\tab\n"); break;
        case '\n': printf("#\\newline\n"); break;
        case '\r': printf("#\\return\n"); break;
        case ' ': printf("#\\space\n"); break;
        default:
            printf("#\\%c\n", c);
        }
    }
    else if ((val & BOOL_MASK) == BOOL_TAG) {
        if ((val >> BOOL_SHIFT) == 1) {
            printf("#t\n");
        } else {
            printf("#f\n");
        }
    }
    else if (val == EMPTY_LIST) {
        printf("()\n");
    }
    return 0;
}
