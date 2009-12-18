#!bin/python

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

def primcall_p(x):
    if not isinstance(x, List): return False
    if not isinstance(x[0], Symbol): return False
    return  x[0][0] in ['$fxadd1', '$fixnum->char', '$char->fixnum', 'fixnum?', '$fxzero?',
                        'null?', 'boolean?', 'char?', 'not', '$fxlognot']

def emit_primcall(x, f):
    s = x[0][0]
    if s == '$fxadd1':
        emit_expr(x[1], f)
        print >>f, "    addl $%d, %%eax" % immediate_rep(1)
    elif s == '$fixnum->char':
        emit_expr(x[1], f)
        print >>f, "    sall $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT)
        print >>f, "    orl $%d, %%eax" % CHAR_TAG
    elif s == '$char->fixnum':
        emit_expr(x[1], f)
        print >>f, "    shrl $%d, %%eax" % (CHAR_SHIFT - FIXNUM_SHIFT)
    elif s == 'fixnum?':
        emit_expr(x[1], f)
        print >>f, "    and $%d, %%al" % FIXNUM_MASK
        print >>f, "    cmp $%d, %%al" % FIXNUM_TAG
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == 'boolean?':
        emit_expr(x[1], f)
        print >>f, "    and $%d, %%al" % BOOL_MASK
        print >>f, "    cmp $%d, %%al" % BOOL_TAG
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == 'char?':
        emit_expr(x[1], f)
        print >>f, "    and $%d, %%al" % CHAR_MASK
        print >>f, "    cmp $%d, %%al" % CHAR_TAG
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == '$fxzero?':
        emit_expr(x[1], f)
        print >>f, "    cmpl $0, %eax"
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == 'null?':
        emit_expr(x[1], f)
        print >>f, "    cmpl $%d, %%eax" % EMPTY_LIST
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == 'not':
        emit_expr(x[1], f)
        print >>f, "    cmpl $%d, %%eax" % BOOL_FALSE
        print >>f, "    sete %al"
        print >>f, "    movzbl %al, %eax"
        print >>f, "    sal $%d, %%al" % BOOL_SHIFT
        print >>f, "    or $%d, %%al" % BOOL_TAG
    elif s == '$fxlognot':
        emit_expr(x[1], f)
        print >>f, "    xorl $%d, %%eax" % 0xfffffffc
    else:
        raise Exception("Unknown primcall: %s" % s)

def emit_expr(x, f):
    if immediate_p(x):
        print >>f, "    movl $%d, %%eax" % immediate_rep(x)
    elif primcall_p(x):
        emit_primcall(x, f)
    else:
        raise Exception("Unknown value: %s" % (x,))

def compile_program(x, text, f):
    # print "Compiling: %s" % x
    emit_function_header("scheme_entry", f)
    emit_expr(x, f)
    print >>f, "    ret"

def emit_function_header(function_name, f):
    print >> f, ".globl _%s" % function_name
    print >> f, "_%s:" % function_name


def compile_and_run(parse, text):
    with open("stst.s", "w+") as f:
        compile_program(parse, text, f)

    # gcc -o stst runtime.c stst.s
    r = subprocess.call("gcc -o stst runtime.c stst.s".split())
    assert r==0, "Compile failed: [%s]" % (text,)
    # ./stst > stst.out
    p = subprocess.Popen(["./stst"], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    if output.endswith("\n"):
        output = output[:-1]
    assert p.returncode==0, "Run failed: [%s]" % (text,)
    return output
