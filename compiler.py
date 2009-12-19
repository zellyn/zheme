import itertools
import subprocess
from parser import Symbol, List, Char

EMPTY_LIST = 0b00101111 # 47 == 0x2f

FIXNUM_SHIFT = 2
FIXNUM_MASK  = 0b11
FIXNUM_TAG   = 0b00

CHAR_SHIFT = 8
CHAR_MASK  = 0b11111111
CHAR_TAG   = 0b00001111

BOOL_SHIFT = 7
BOOL_MASK  = 0b1111111
BOOL_TAG   = 0b0011111
BOOL_TRUE  = (1<<BOOL_SHIFT) | BOOL_TAG
BOOL_FALSE = (0<<BOOL_SHIFT) | BOOL_TAG

WORD_SIZE = 4

__labels = itertools.count()
def get_label():
    return "L_%d" % next(__labels)

def immediate_p(x):
    return isinstance(x, (int, Char)) or (List()==x)

def immediate_rep(x):
    if isinstance(x, bool):
        return (x << BOOL_SHIFT) | BOOL_TAG
    elif isinstance(x, int):
        return (x << FIXNUM_SHIFT) | FIXNUM_TAG
    elif isinstance(x, Char):
        return (ord(x[0]) << CHAR_SHIFT) | CHAR_TAG
    elif (List()==x):
        return EMPTY_LIST
    else:
        raise Exception("Unknown immediate value: %s" % (x,))

def func_p(x, names):
    return isinstance(x, List) and isinstance(x[0], Symbol) and x[0][0] in names

def primcall_p(x):
    return func_p(x,  ['$fxadd1', '$fxsub1', '$fixnum->char', '$char->fixnum', 'fixnum?',
                       '$fxzero?', 'null?', 'boolean?', 'char?', 'not', '$fxlognot'])

def binary_p(x):
    return func_p(x,  ['fx+'])

def and_p(x):
    return func_p(x, ['and'])

def or_p(x):
    return func_p(x, ['or'])

def if_p(x):
    return func_p(x, ['if'])

def emit_binary(x, si, f):
    s = x[0][0]
    if s == 'fx+':
        emit_expr(x[1], si, f)
        print("    movl %%eax, %d(%%esp)" % si, file=f)
        emit_expr(x[2], si - WORD_SIZE, f)
        print("    addl %d(%%esp), %%eax" % si, file=f)
    else:
        raise Exception("Unknown binary: %s" % s)

def emit_primcall(x, si, f):
    s = x[0][0]
    if s == '$fxadd1':
        emit_expr(x[1], si, f)
        print("    addl $%d, %%eax" % immediate_rep(1), file=f)
    elif s == '$fxsub1':
        emit_expr(x[1], si, f)
        print("    subl $%d, %%eax" % immediate_rep(1), file=f)
    elif s == '$fixnum->char':
        emit_expr(x[1], si, f)
        print("    sall $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT), file=f)
        print("    orl $%d, %%eax" % CHAR_TAG, file=f)
    elif s == '$char->fixnum':
        emit_expr(x[1], si, f)
        print("    shrl $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT), file=f)
    elif s == 'fixnum?':
        emit_expr(x[1], si, f)
        print("    and $%d, %%al" % FIXNUM_MASK, file=f)
        print("    cmp $%d, %%al" % FIXNUM_TAG, file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == 'boolean?':
        emit_expr(x[1], si, f)
        print("    and $%d, %%al" % BOOL_MASK, file=f)
        print("    cmp $%d, %%al" % BOOL_TAG, file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == 'char?':
        emit_expr(x[1], si, f)
        print("    and $%d, %%al" % CHAR_MASK, file=f)
        print("    cmp $%d, %%al" % CHAR_TAG, file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == '$fxzero?':
        emit_expr(x[1], si, f)
        print("    cmpl $0, %eax", file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == 'null?':
        emit_expr(x[1], si, f)
        print("    cmpl $%d, %%eax" % EMPTY_LIST, file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == 'not':
        emit_expr(x[1], si, f)
        print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
        print("    sete %al", file=f)
        print("    movzbl %al, %eax", file=f)
        print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
        print("    or $%d, %%al" % BOOL_TAG, file=f)
    elif s == '$fxlognot':
        emit_expr(x[1], si, f)
        print("    xorl $%d, %%eax" % 0xfffffffc, file=f)
    else:
        raise Exception("Unknown primcall: %s" % s)

def emit_and(exprs, si, f):
    if not exprs:
        emit_expr(True, si, f)
        return
    over_label = get_label()
    for expr in exprs[:-1]:
        emit_expr(expr, si, f)
        print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
        print("    je %s" % over_label, file=f)
    emit_expr(exprs[-1], si, f)
    print("%s:" % over_label, file=f)

def emit_or(exprs, si, f):
    if not exprs:
        emit_expr(False, si, f)
        return
    over_label = get_label()
    for expr in exprs[:-1]:
        emit_expr(expr, si, f)
        print("    cmpl $%d, %%eax" % BOOL_TRUE, file=f)
        print("    je %s" % over_label, file=f)
    emit_expr(exprs[-1], si, f)
    print("%s:" % over_label, file=f)

def emit_if(exprs, si, f):
    false_label = get_label()
    over_label = get_label()
    emit_expr(exprs[0], si, f)
    print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
    print("    je %s" % false_label, file=f)
    emit_expr(exprs[1], si, f)
    print("jmp %s" % over_label, file=f)
    print("%s:" % false_label, file=f)
    emit_expr(exprs[2], si, f)
    print("%s:" % over_label, file=f)

def emit_expr(x, si, f):
    if immediate_p(x):
        print("    movl $%d, %%eax" % immediate_rep(x), file=f)
    elif primcall_p(x):
        emit_primcall(x, si, f)
    elif binary_p(x):
        emit_binary(x, si, f)
    elif and_p(x):
        emit_and(x[1:], si, f)
    elif or_p(x):
        emit_or(x[1:], si, f)
    elif if_p(x):
        emit_if(x[1:], si, f)
    else:
        raise Exception("Unknown value: %s" % (x,))

def compile_program(x, text, f):
    # print "Compiling: %s" % x
    emit_function_header("L_scheme_entry", f)
    emit_expr(x, -WORD_SIZE, f)           # start at stack-4 (stack-0 is return addr)
    print("    ret", file=f)

    # wrapper - called by C, passed address of scheme stack
    emit_function_header("_scheme_entry", f)
    print("    movl %esp, %ecx", file=f)      # save off c stack ptr
    print("    movl 4(%esp), %esp", file=f)   # use scheme stack
    print("    call L_scheme_entry", file=f)  # call actual compiled expression
    print("    movl %ecx, %esp", file=f)      # restore c stack ptr
    print("    ret", file=f)

def emit_function_header(function_name, f):
    print(".globl %s" % function_name, file=f)
    print("%s:" % function_name, file=f)


def compile_and_run(parse, text):
    with open("stst.s", "w+") as f:
        compile_program(parse, text, f)

    # gcc -o stst runtime.c stst.s
    r = subprocess.call("gcc -o stst runtime.c stst.s".split())
    assert r==0, "Compile failed: [%s]" % (text,)
    # ./stst > stst.out
    p = subprocess.Popen(["./stst"], stdout=subprocess.PIPE)
    output = p.communicate()[0].decode('utf-8')
    if output.endswith("\n"):
        output = output[:-1]
    assert p.returncode==0, "Run failed: [%s]" % (text,)
    return output
