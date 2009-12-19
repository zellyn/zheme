/* a simple driver for scheme_entry */
#include <stdio.h>
#include <sys/mman.h>

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

static char* allocate_protected_space(int size) {
    int page = getpagesize();
    int status;
    int aligned_size = ((size + page - 1) / page) * page;
    char* p = mmap(0, aligned_size + 2 * page,
                   PROT_READ | PROT_WRITE,
                   MAP_ANON | MAP_PRIVATE,
                   0, 0);
    if (p == MAP_FAILED) {
        printf("*** Error allocating ***\n"); // do something more sensible
    }
    status = mprotect(p, page, PROT_NONE);
    if (status != 0) {
        printf("*** Error protecting first page ***\n"); // do something more sensible
    }
    status = mprotect(p + page + aligned_size, page, PROT_NONE);
    if (status != 0) {
        printf("*** Error protecting last page ***\n"); // do something more sensible
    }
    return (p + page);
}

static void deallocate_protected_space(char* p, int size) {
    int page = getpagesize();
    int status;
    int aligned_size = ((size + page - 1) / page) * page;
    status = munmap(p - page, aligned_size + 2 * page);
    if (status != 0) {
        printf("*** Error deallocating ***\n"); // do something more sensible
    }
}

void print_val(int val) {
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
}

int main(int argc, char** argv) {
    int stack_size = (16 * 4096);  /* holds 16K cells */
    char* stack_top = allocate_protected_space(stack_size);
    char* stack_base = stack_top + stack_size;

    int val = scheme_entry(stack_base);
    print_val(val);

    deallocate_protected_space(stack_top, stack_size);
    return 0;
}
