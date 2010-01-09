import itertools
import subprocess
from parser import Symbol, List, Char

WORD_SIZE = 4

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

PAIR_TAG     = 0b001
PAIR_MASK    = 0b111
CAR_OFFSET = 0
CDR_OFFSET = 4

PAIR_SIZE = 2 * WORD_SIZE
CAR_TAG_OFFSET = CAR_OFFSET - PAIR_TAG # -1
CDR_TAG_OFFSET = CDR_OFFSET - PAIR_TAG # 3

CLOSURE_TAG  = 0b010
CLOSURE_MASK = 0b111
SYMBOL_TAG   = 0b011
SYMBOAL_MASK = 0b111
VECTOR_TAG   = 0b101
VECTOR_MASK  = 0b111
STRING_TAG   = 0b110
STRING_MASK  = 0b111

VECTOR_SIZE_OFFSET = -VECTOR_TAG
VECTOR_ZERO_OFFSET = VECTOR_SIZE_OFFSET + WORD_SIZE

__known_ops = dict()

def op(name, min_args, max_args=-1):
    def decorate(f):
        __known_ops[name] = (f, min_args, max_args)
        return f
    return decorate

def emit_op(name, expr, si, env, f):
    func, min_args, max_args = __known_ops.get(name, (None, None, None))
    if func is None:
        raise Exception("Unknown op: %s" % name)

    if max_args==-1:
        assert len(expr)-1==min_args, "'%s' expects %d args: %s" % (name, min_args, expr)
    else:
        assert len(expr)-1>=min_args, "Expected at least %d args: %s" % (min_args, expr)
        if max_args is not None:
            assert len(expr)-1<=max_args, "Expected at most %d args: %s" % (max_args, expr)
    func(expr, si, env, f)

__labels = itertools.count()
def get_label():
    return "L_%d" % next(__labels)

def immediate_p(x):
    return isinstance(x, (int, Char)) or (List()==x)

def variable_name(x):
    if not isinstance(x, Symbol):
        return None
    return x[0]

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
def emit_fx_plus(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    addl %d(%%esp), %%eax" % si)

@op('fx-', 2)
def emit_fx_minus(x, si, env, f):
    emit_expr(x[2], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[1], si - WORD_SIZE, env, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)

@op('fx*', 2)
def emit_fx_mul(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    sarl $%d, %%eax" % FIXNUM_SHIFT)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    imull %d(%%esp), %%eax" % si)

@op('fxlogor', 2)
def emit_fx_logor(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    orl %d(%%esp), %%eax" % si)

@op('fxlognot', 1)
def emit_fx_lognot(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    xorl $%d, %%eax" % (FULL_WORD-FIXNUM_MASK))

@op('fxlogand', 2)
def emit_fx_logand(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    andl %d(%%esp), %%eax" % si)

@op('fx=', 2)
def emit_fx_eq(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    cmpl %d(%%esp), %%eax" % si)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx<', 2)
def emit_fx_lt(x, si, env, f):
    emit_expr(x[2], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[1], si - WORD_SIZE, env, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)
    emit(f, "    sets %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx<=', 2)
def emit_fx_lte(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[2], si - WORD_SIZE, env, f)
    emit(f, "    subl %d(%%esp), %%eax" % si)
    emit(f, "    setns %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('fx>', 2)
def emit_fx_gt(x, si, env, f):
    emit_fx_lt(List(x[0],x[2],x[1]), si, env, f)

@op('fx>=', 2)
def emit_fx_gte(x, si, env, f):
    emit_fx_lte(List(x[0],x[2],x[1]), si, env, f)

@op('eq?', 2)
def emit_eq(x, si, env, f):
    emit_expr(x[2], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si)
    emit_expr(x[1], si - WORD_SIZE, env, f)
    emit(f, "    cmpl %d(%%esp), %%eax" % si)
    emit(f, "    setz %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('$fxadd1', 1)
def emit_fxadd1(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    addl $%d, %%eax" % immediate_rep(1))

@op('$fxsub1', 1)
def emit_fxsub1(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    subl $%d, %%eax" % immediate_rep(1))

@op('$fixnum->char', 1)
def emit_fixnum_char(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    shll $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT))
    emit(f, "    orl $%d, %%eax" % CHAR_TAG)

@op('$char->fixnum', 1)
def emit_char_fixnum(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    shrl $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT))

@op('fixnum?', 1)
def emit_fixnum_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    and $%d, %%al" % FIXNUM_MASK)
    emit(f, "    cmp $%d, %%al" % FIXNUM_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('boolean?', 1)
def emit_boolean_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    and $%d, %%al" % BOOL_MASK)
    emit(f, "    cmp $%d, %%al" % BOOL_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('char?', 1)
def emit_char_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    and $%d, %%al" % CHAR_MASK)
    emit(f, "    cmp $%d, %%al" % CHAR_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('$fxzero?', 1)
def emit_fxzero_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    cmpl $0, %eax")
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('null?', 1)
def emit_null_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    cmpl $%d, %%eax" % EMPTY_LIST)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('not', 1)
def emit_not(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('$fxlognot', 1)
def emit_fxlognot(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    xorl $%d, %%eax" % 0xfffffffc)

@op('and', 0, None)
def emit_and(expr, si, env, f):
    if len(expr)==1:
        emit_expr(True, si, env, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, env, f)
        emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
        emit(f, "    je %s" % over_label)
    emit_expr(expr[-1], si, env, f)
    emit(f, "%s:" % over_label)

@op('or', 0, None)
def emit_or(expr, si, env, f):
    if len(expr)==1:
        emit_expr(False, si, env, f)
        return
    over_label = get_label()
    for subex in expr[1:-1]:
        emit_expr(subex, si, env, f)
        emit(f, "    cmpl $%d, %%eax" % BOOL_TRUE)
        emit(f, "    je %s" % over_label)
    emit_expr(expr[-1], si, env, f)
    emit(f, "%s:" % over_label)

@op('if', 3)
def emit_if(expr, si, env, f):
    false_label = get_label()
    over_label = get_label()
    emit_expr(expr[1], si, env, f)
    emit(f, "    cmpl $%d, %%eax" % BOOL_FALSE)
    emit(f, "    je %s" % false_label)
    emit_expr(expr[2], si, env, f)
    emit(f, "jmp %s" % over_label)
    emit(f, "%s:" % false_label)
    emit_expr(expr[3], si, env, f)
    emit(f, "%s:" % over_label)

@op('let', 2, None)
def emit_let(expr, si, env, f):
    bindings = expr[1]
    new_env = dict(env)
    for var, value in bindings:
        name = variable_name(var)
        assert name is not None, "Can't assign to %s" % var
        emit_expr(value, si, env, f)
        emit(f, "    movl %%eax, %d(%%esp)" % si) # stack save
        new_env[name] = si
        si -= WORD_SIZE
    for inner in expr[2:]:
        emit_expr(inner, si, new_env, f)

@op('pair?', 1)
def emit_pair_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    and $%d, %%al" % PAIR_MASK)
    emit(f, "    cmp $%d, %%al" % PAIR_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('vector?', 1)
def emit_vector_p(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    and $%d, %%al" % VECTOR_MASK)
    emit(f, "    cmp $%d, %%al" % VECTOR_TAG)
    emit(f, "    sete %al")
    emit(f, "    movzbl %al, %eax")
    emit(f, "    shl $%d, %%al" % BOOL_SHIFT)
    emit(f, "    or $%d, %%al" % BOOL_TAG)

@op('cons', 2)
def emit_cons(x, si, env, f):
    emit_expr(x[2], si, env, f)
    emit(f, "    movl %%eax, %d(%%esp)" % si) # save cdr
    emit_expr(x[1], si - WORD_SIZE, env, f)
    emit(f, "    movl %%eax, %d(%%ebp)" % CAR_OFFSET)
    emit(f, "    movl %d(%%esp), %%eax" % si) # restore cdr
    emit(f, "    movl %%eax, %d(%%ebp)" % CDR_OFFSET)
    emit(f, "    movl %ebp, %eax")
    emit(f, "    addl $%d, %%ebp" % PAIR_SIZE)
    emit(f, "    orl $%d, %%eax" % PAIR_TAG)

@op('make-vector', 1)
def emit_make_vector(x, si, env, f):
    emit(f, "# make-vector")
    # length in eax
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %ebp, %edx") # save vector address
    emit(f, "    movl %eax, (%ebp)") # save length
    emit(f, "    addl $%d, %%ebp" % WORD_SIZE)
    assert 1 << FIXNUM_SHIFT == WORD_SIZE, "Assume no shifts necessary for byte-length of vector"
    emit(f, "    addl %eax, %ebp")
    emit(f, "    addl $7, %ebp")
    emit(f, "    andl $%d, %%ebp" % (FULL_WORD - 7))
    emit(f, "    movl %edx, %eax")
    emit(f, "    orl $%d, %%eax" % VECTOR_TAG)

@op('vector-length', 1)
def emit_vector_length(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %d(%%eax), %%eax" % VECTOR_SIZE_OFFSET)

@op('vector-set!', 3)
def emit_vector_set(x, si, env, f):
    emit(f, "# vector-set!")
    # vector, position, value
    emit_expr(x[1], si, env, f) # vector address
    emit(f, "    addl $%d, %%eax" % VECTOR_ZERO_OFFSET)
    emit(f, "    movl %%eax, %d(%%esp)" % si) # save vector address
    emit_expr(x[2], si - WORD_SIZE, env, f) # position
    assert 1 << FIXNUM_SHIFT == WORD_SIZE, "Assume no shifts necessary for indexing into vector"
    emit(f, "    addl %%eax, %d(%%esp)" % si) # add to address
    emit_expr(x[3], si - WORD_SIZE, env, f) # value
    emit(f, "    movl %d(%%esp), %%edx" % si)
    emit(f, "    movl %eax, (%edx)")

@op('vector-ref', 2)
def emit_vector_ref(x, si, env, f):
    emit(f, "# vector-ref")
    # vector, position
    emit_expr(x[1], si, env, f) # vector address
    emit(f, "    addl $%d, %%eax" % VECTOR_ZERO_OFFSET)
    emit(f, "    movl %%eax, %d(%%esp)" % si) # save vector address
    emit_expr(x[2], si - WORD_SIZE, env, f) # position
    assert 1 << FIXNUM_SHIFT == WORD_SIZE, "Assume no shifts necessary for indexing into vector"
    emit(f, "    addl %%eax, %d(%%esp)" % si) # add to address
    emit(f, "    movl %d(%%esp), %%edx" % si)
    emit(f, "    movl (%edx), %eax")

@op('car', 1)
def emit_car(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %d(%%eax), %%eax" % CAR_TAG_OFFSET)

@op('cdr', 1)
def emit_cdr(x, si, env, f):
    emit_expr(x[1], si, env, f)
    emit(f, "    movl %d(%%eax), %%eax" % CDR_TAG_OFFSET)

def emit_variable_ref(x, env, f):
    name = variable_name(x)
    if name not in env:
        raise Exception("Unknown variable: '%s'")
    index = env[name]
    emit(f, "    movl %d(%%esp), %%eax" % index)

def emit_expr(x, si, env, f):
    if immediate_p(x):
        emit(f, "    movl $%d, %%eax" % immediate_rep(x))
    elif variable_name(x):
        emit_variable_ref(x, env, f)
    else:
        op = get_op(x)
        if op is not None:
            emit_op(op, x, si, env, f)
        else:
            raise Exception("Unknown value: %s" % (x,))

def compile_program(x, text, f):
    # print "Compiling: %s" % x
    emit_function_header("L_scheme_entry", f)
    emit_expr(x, -WORD_SIZE, {}, f)           # start at stack-4 (stack-0 is return addr)
    emit(f, "    ret")

    # wrapper - called by C, passed address of scheme stack
    emit_function_header("_scheme_entry", f)
    # page 39 of (b)
    emit(f, "    movl 4(%esp), %ecx")   # ARG: REGISTER STRUCT
    emit(f, "    movl %ebx, 4(%ecx)")   # save ebx
    emit(f, "    movl %esi, 16(%ecx)")  # save esi
    emit(f, "    movl %edi, 20(%ecx)")  # save edi
    emit(f, "    movl %ebp, 24(%ecx)")  # save ebp
    emit(f, "    movl %esp, 28(%ecx)")  # save esp
    emit(f, "    movl 12(%esp), %ebp")  # ARG: HEAP
    emit(f, "    movl 8(%esp), %esp")   # ARG: STACK
    emit(f, "    call L_scheme_entry")  # call actual compiled expression
    emit(f, "    movl 4(%ecx), %ebx")   # restore ebx
    emit(f, "    movl 16(%ecx), %esi")   # restore esi
    emit(f, "    movl 20(%ecx), %edi")   # restore edi
    emit(f, "    movl 24(%ecx), %ebp")   # restore ebp
    emit(f, "    movl 28(%ecx), %esp")   # restore esp
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
