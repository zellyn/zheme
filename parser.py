from lepl import *

# Parser uses terminology and (more or less) grammar from r5rs to keep
# things straight. See
# http://www.schemers.org/Documents/Standards/R5RS/HTML/r5rs-Z-H-10.html#%_sec_7.1.1
# (although the PDF version is much easier to read).

# Work around nested Node equality bug in lepl 3.3.3
# http://code.google.com/p/lepl/issues/detail?id=17
class NodePlus(Node):
    def __ne__(self, other):
        return not (self==other)

class Symbol(NodePlus): pass
class List(NodePlus): pass
class DotList(NodePlus): pass
class Char(NodePlus): pass

def float_or_int(s):
    if '.' in s:
        return float(s)
    else:
        return int(s)

def to_bool(s):
    return s == '#t'

def make_char(s):
    SPECIALS = {
        'space': ' ',
        'newline': '\n',
        'return': '\r',
        'tab': '\t',
        }

    if len(s) == 3:
        return Char(s[2])
    return Char(SPECIALS.get(s[2:]))


s_character = Or(Literal('#\\newline'), Literal('#\\tab'), Literal('#\\space'),
                 Literal('#\\return'), DfaRegexp('#\\\\[^ \r\n\t\f\v]')) >> make_char
s_boolean = (Literal('#f') | Literal('#t')) >> to_bool
s_string = String()
s_number = Float() >> float_or_int

s_special_initial = DfaRegexp('[!\\$%&\\*/:<=>\\?\\^_~]')
s_letter = Letter()
s_initial = s_letter | s_special_initial
s_peculiar_identifier = Literal('+') | Literal('-') | Literal('...')
s_special_subsequent = DfaRegexp('[\\+\\.@\\-]')
s_digit = Digit()
s_subsequent = s_initial | s_digit | s_special_subsequent
s_identifier = Word(s_initial, s_subsequent) | s_peculiar_identifier

s_datum = Delayed()
s_abbrev_prefix = Literal("'") | Literal("`") | Literal(",") | Literal(",@")
s_abbreviation = s_abbrev_prefix & s_datum
s_list = Or(
    (~Literal('(') & ~Whitespace()[:] & ~Literal(')')) > List,
    (~Literal('(') & s_datum[1:] & ~Literal(')')) > List,
    (~Literal('(') & (s_datum[1:] & ~Literal('.') & s_datum & ~Literal(')')) > DotList),
    (~Literal('[') & ~Whitespace()[:] & ~Literal(']')) > List,
    (~Literal('[') & s_datum[1:] & ~Literal(']')) > List,
    (~Literal('[') & (s_datum[1:] & ~Literal('.') & s_datum & ~Literal(']')) > DotList),
    s_abbreviation)
s_compound_datum = s_list # | s_vector
s_symbol = s_identifier > Symbol
s_simple_datum = s_boolean | s_number | s_character | s_string | s_symbol
s_datum += ~Whitespace()[:] & (s_simple_datum | s_compound_datum) & ~Whitespace()[:]

parser = s_datum.string_parser()

def parse(s):
    p = parser(s)
    if p is not None:
        return p[0]
    else:
        raise Exception("Cannot parse '%s'" % s)
