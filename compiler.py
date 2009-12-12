#!bin/python
def compile_program(x):
    emit_function_header("scheme_entry")
    print "    movl $%d, %%eax" % x
    print "    ret"

def emit_function_header(function_name):
    print ".globl _%s" % function_name
    print "_%s:" % function_name

compile_program(42)
