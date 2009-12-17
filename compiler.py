#!bin/python

import subprocess
from parser import Symbol, List, Char

EMPTY_LIST = 0b00101111 # 47 == 0x2f
FIXNUM_SHIFT = 2
FIXNUM_MASK = 0b11
FIXNUM_TAG  = 0b00

def compile_program(x, text, f):
    emit_function_header("scheme_entry", f)
    if isinstance(x, int):
        x <<= FIXNUM_SHIFT
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
