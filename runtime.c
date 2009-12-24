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

#define PAIR_TAG 0x01
#define PAIR_MASK 0x07


typedef struct {
    void* eax;    /* 0    scratch  */
    void* ebx;    /* 4    preserve */
    void* ecx;    /* 8    scratch  */
    void* edx;    /* 12   scratch  */
    void* esi;    /* 16   preserve */
    void* edi;    /* 20   preserve */
    void* ebp;    /* 24   preserve */
    void* esp;    /* 28   preserve */
} context;

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

int pair_p(int val) {
    return ((val & PAIR_MASK) == PAIR_TAG);
}

void print_expr(int val);

void print_list(int val) {
    int* addr = (int*)(val - PAIR_TAG);
    printf("(");
    print_expr(addr[0]);
    while (pair_p(addr[1])) {
        printf(" ");
        addr = (int*)(addr[1] - PAIR_TAG);
        print_expr(addr[0]);
    }
    if (addr[1]!=EMPTY_LIST) {
        printf(" . ");
        print_expr(addr[1]);
    }
    printf(")");
}

void print_expr(int val) {
    if ((val & FIXNUM_MASK) == FIXNUM_TAG) {
        printf("%d", val >> FIXNUM_SHIFT);
    }
    else if ((val & CHAR_MASK) == CHAR_TAG) {
        int c = val >> CHAR_SHIFT;
        switch (c) {
        case '\t': printf("#\\tab"); break;
        case '\n': printf("#\\newline"); break;
        case '\r': printf("#\\return"); break;
        case ' ': printf("#\\space"); break;
        default:
            printf("#\\%c", c);
        }
    }
    else if ((val & BOOL_MASK) == BOOL_TAG) {
        if ((val >> BOOL_SHIFT) == 1) {
            printf("#t");
        } else {
            printf("#f");
        }
    }
    else if (val == EMPTY_LIST) {
        printf("()");
    }
    else if (pair_p(val)) {
        print_list(val);
    }
    else {
        printf("UNKNOWN!");
    }
}

void print_val(int val) {
    print_expr(val);
    printf("\n");
}

int main(int argc, char** argv) {
    int stack_size = (16 * 4096);  /* holds 16K cells */
    int heap_size = (16 * 4096);   /* ditto */
    char* stack_top = allocate_protected_space(stack_size);
    char* stack_base = stack_top + stack_size;
    char* heap = allocate_protected_space(heap_size);

    context ctxt;
    int val = scheme_entry(&ctxt, stack_base, heap);
    print_val(val);

    deallocate_protected_space(heap, heap_size);
    deallocate_protected_space(stack_top, stack_size);
    return 0;
}
