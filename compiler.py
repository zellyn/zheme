import itertools
import subprocess
from parser import Symbol, List, Char

FULL_WORD = 0xffffffff

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

def get_op(x):
    if isinstance(x, List) and isinstance(x[0], Symbol):
        return x[0][0]
    return None

def emit(f, s):
    print(s, file=f)

@op('fx+', 2)
def emit_fx_plus(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    addl %d(%%esp), %%eax" % si)

@op('fx-', 2)
def emit_fx_minus(x, si, f):
    emit_expr(x[2], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[1], si - WORD_SIZE, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)

@op('fx*', 2)
def emit_fx_mul(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    sarl $%d, %%eax" % FIXNUM_SHIFT)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    imull %d(%%esp), %%eax" % si)

@op('fxlogor', 2)
def emit_fx_logor(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    orl %d(%%esp), %%eax" % si)

@op('fxlognot', 1)
def emit_fx_lognot(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    xorl $%d, %%eax" % (FULL_WORD-FIXNUM_MASK))

@op('fxlogand', 2)
def emit_fx_logand(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    andl %d(%%esp), %%eax" % si)

@op('fx=', 2)
def emit_fx_eq(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    cmpl %d(%%esp), %%eax" % si)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx<', 2)
def emit_fx_lt(x, si, f):
    emit_expr(x[2], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[1], si - WORD_SIZE, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)
    emit(f, "    sets %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx<=', 2)
def emit_fx_lte(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)
    emit(f, "    setns %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx>', 2)
def emit_fx_gt(x, si, f):
    emit_fx_lt(List(x[0],x[2],x[1]), si, f)

@op('fx>=', 2)
def emit_fx_gte(x, si, f):
    emit_fx_lte(List(x[0],x[2],x[1]), si, f)

@op('$fxadd1', 1)
def emit_fxadd1(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    addl $%d, %%eax" % immediate_rep(1))

@op('$fxsub1', 1)
def emit_fxsub1(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    subl $%d, %%eax" % immediate_rep(1))

@op('$fixnum->char', 1)
def emit_fixnum_char(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    shll $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT))
    emit(f, "    orl $%d, %%eax" % CHAR_TAG)

@op('$char->fixnum', 1)
def emit_char_fixnum(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    shrl $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT))

@op('fixnum?', 1)
def emit_fixnum_p(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    and $%d, %%al" % FIXNUM_MASK)
    emit(f, "    cmp $%d, %%al" % FIXNUM_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('boolean?', 1)
def emit_boolean_p(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    and $%d, %%al" % BOOL_MASK)
    emit(f, "    cmp $%d, %%al" % BOOL_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('char?', 1)
def emit_char_p(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    and $%d, %%al" % CHAR_MASK)
    emit(f, "    cmp $%d, %%al" % CHAR_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('$fxzero?', 1)
def emit_fxzero_p(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    cmpl $0, %eax")
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('null?', 1)
def emit_null_p(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    cmpl $%d, %%eax" % EMPTY_LIST)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('not', 1)
def emit_not(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('$fxlognot', 1)
def emit_fxlognot(x, si, f):
    emit_expr(x[1], si, f)
    emit(f, "    xorl $%d, %%eax" % 0xfffffffc)

@op('and', 0, None)
def emit_and(expr, si, f):
    if len(expr)==1:
        emit_expr(True, si, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, f)
        emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
        emit(f, "    je %s" % over_label)
    emit_expr(expr[-1], si, f)
    emit(f, "%s:" % over_label)

@op('or', 0, None)
def emit_or(expr, si, f):
    if len(expr)==1:
        emit_expr(False, si, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, f)
        emit(f, "    cmpl $%d, %%eax" % BOOL_TRUE)
        emit(f, "    je %s" % over_label)
    emit_expr(expr[-1], si, f)
    emit(f, "%s:" % over_label)

@op('if', 3)
def emit_if(expr, si, f):
    false_label = get_label()
    over_label = get_label()
    emit_expr(expr[1], si, f)
    emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
    emit(f, "    je %s" % false_label)
    emit_expr(expr[2], si, f)
    emit(f, "jmp %s" % over_label)
    emit(f, "%s:" % false_label)
    emit_expr(expr[3], si, f)
    emit(f, "%s:" % over_label)

def emit_expr(x, si, f):
    if immediate_p(x):
        emit(f, "    movl $%d, %%eax" % immediate_rep(x))
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
    emit(f, "    ret")

    # wrapper - called by C, passed address of scheme stack
    emit_function_header("_scheme_entry", f)
    emit(f, "    movl %esp, %ecx")      # save off c stack ptr
    emit(f, "    movl 4(%esp), %esp")   # use scheme stack
    emit(f, "    call L_scheme_entry")  # call actual compiled expression
    emit(f, "    movl %ecx, %esp")      # restore c stack ptr
    emit(f, "    ret")

def emit_function_header(function_name, f):
    emit(f, ".globl %s" % function_name)
    emit(f, "%s:" % function_name)


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
