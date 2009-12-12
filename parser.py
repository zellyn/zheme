from lepl import *

class Symbol(Node): pass
class List(Node): pass
class DotList(Node): pass
class Char(Node): pass

def float_or_int(s):
    if '.' in s:
        return float(s)
    else:
        return int(s)

def to_bool(s):
    return s == '#t'

s_character = Or(Literal('#\\newline'), Literal('#\\tab'), Literal('#\\space'),
                 Literal('#\\return'), DfaRegexp('#\\\\[^ \r\n\t\f\v]')) > Char
s_character = Literal('#\\newline')
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
    s_abbreviation)
s_compound_datum = s_list # | s_vector
s_symbol = s_identifier > Symbol
s_simple_datum = s_boolean | s_number | s_character | s_string | s_symbol
s_datum += ~Whitespace()[:] & (s_simple_datum | s_compound_datum) & ~Whitespace()[:]

def parse(s):
    p = s_datum.parse(s)
    if p is not None:
        return p[0]
    else:
        raise Exception("Cannot parse '%s'" % s)
