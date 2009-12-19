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

__known_ops = dict()

def op(name, min_args, max_args=-1):
    def decorate(f):
        __known_ops[name] = (f, min_args, max_args)
        return f
    return decorate

def emit_op(name, expr, si, f):
    func, min_args, max_args = __known_ops.get(name, (None, None, None))
    if func is None:
        raise Exception("Unknown op: %s" % name)

    if max_args==-1:
        assert len(expr)-1==min_args, "Expected %d args: %s" % (min_args, expr)
    else:
        assert len(expr)-1>=min_args, "Expected at least %d args: %s" % (min_args, expr)
        if max_args is not None:
            assert len(expr)-1<=max_args, "Expected at most %d args: %s" % (max_args, expr)
    func(expr, si, f)

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

def get_op(x):
    if isinstance(x, List) and isinstance(x[0], Symbol):
        return x[0][0]
    return None

@op('fx+', 2)
def emit_fx_plus(x, si, f):
    emit_expr(x[1], si, f)
    print("    movl %%eax, %d(%%esp)" % si, file=f)
    emit_expr(x[2], si - WORD_SIZE, f)
    print("    addl %d(%%esp), %%eax" % si, file=f)

@op('$fxadd1', 1)
def emit_fxadd1(x, si, f):
    emit_expr(x[1], si, f)
    print("    addl $%d, %%eax" % immediate_rep(1), file=f)

@op('$fxsub1', 1)
def emit_fxsub1(x, si, f):
    emit_expr(x[1], si, f)
    print("    subl $%d, %%eax" % immediate_rep(1), file=f)

@op('$fixnum->char', 1)
def emit_fixnum_char(x, si, f):
    emit_expr(x[1], si, f)
    print("    sall $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT), file=f)
    print("    orl $%d, %%eax" % CHAR_TAG, file=f)

@op('$char->fixnum', 1)
def emit_char_fixnum(x, si, f):
    emit_expr(x[1], si, f)
    print("    shrl $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT), file=f)

@op('fixnum?', 1)
def emit_fixnum_p(x, si, f):
    emit_expr(x[1], si, f)
    print("    and $%d, %%al" % FIXNUM_MASK, file=f)
    print("    cmp $%d, %%al" % FIXNUM_TAG, file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('boolean?', 1)
def emit_boolean_p(x, si, f):
    emit_expr(x[1], si, f)
    print("    and $%d, %%al" % BOOL_MASK, file=f)
    print("    cmp $%d, %%al" % BOOL_TAG, file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('char?', 1)
def emit_char_p(x, si, f):
    emit_expr(x[1], si, f)
    print("    and $%d, %%al" % CHAR_MASK, file=f)
    print("    cmp $%d, %%al" % CHAR_TAG, file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('$fxzero?', 1)
def emit_fxzero_p(x, si, f):
    emit_expr(x[1], si, f)
    print("    cmpl $0, %eax", file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('null?', 1)
def emit_null_p(x, si, f):
    emit_expr(x[1], si, f)
    print("    cmpl $%d, %%eax" % EMPTY_LIST, file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('not', 1)
def emit_not(x, si, f):
    emit_expr(x[1], si, f)
    print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
    print("    sete %al", file=f)
    print("    movzbl %al, %eax", file=f)
    print("    sal $%d, %%al" % BOOL_SHIFT, file=f)
    print("    or $%d, %%al" % BOOL_TAG, file=f)

@op('$fxlognot', 1)
def emit_fxlognot(x, si, f):
    emit_expr(x[1], si, f)
    print("    xorl $%d, %%eax" % 0xfffffffc, file=f)

@op('and', 0, None)
def emit_and(expr, si, f):
    if len(expr)==1:
        emit_expr(True, si, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, f)
        print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
        print("    je %s" % over_label, file=f)
    emit_expr(expr[-1], si, f)
    print("%s:" % over_label, file=f)

@op('or', 0, None)
def emit_or(expr, si, f):
    if len(expr)==1:
        emit_expr(False, si, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, f)
        print("    cmpl $%d, %%eax" % BOOL_TRUE, file=f)
        print("    je %s" % over_label, file=f)
    emit_expr(expr[-1], si, f)
    print("%s:" % over_label, file=f)

@op('if', 3)
def emit_if(expr, si, f):
    false_label = get_label()
    over_label = get_label()
    emit_expr(expr[1], si, f)
    print("    cmpl $%d, %%eax" % BOOL_FALSE, file=f)
    print("    je %s" % false_label, file=f)
    emit_expr(expr[2], si, f)
    print("jmp %s" % over_label, file=f)
    print("%s:" % false_label, file=f)
    emit_expr(expr[3], si, f)
    print("%s:" % over_label, file=f)

def emit_expr(x, si, f):
    if immediate_p(x):
        print("    movl $%d, %%eax" % immediate_rep(x), file=f)
    else:
        op = get_op(x)
        if op is not None:
            emit_op(op, x, si, f)
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
