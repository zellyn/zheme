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


def compile_program(x, text, f):
    # print "Compiling: %s" % x
    emit_function_header("scheme_entry", f)
    if isinstance(x, bool):
        x = (x << BOOL_SHIFT) | BOOL_TAG
    elif isinstance(x, int):
        x = (x << FIXNUM_SHIFT) | FIXNUM_TAG
    elif isinstance(x, Char):
        x = (ord(x[0]) << CHAR_SHIFT) | CHAR_TAG
    elif (List()==x):
        x = EMPTY_LIST
    else:
        raise Exception("Unknown value from [%s]: %s" % (text, x))
    print >>f, "    movl $%d, %%eax" % x
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
