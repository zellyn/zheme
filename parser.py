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


# s_character = (Literal('#\\newline'), Literal('#\\tab'), Literal('#\\space'),
#                Literal('#\\return'), DfaRegexp('#\\\\[^ \r\n\t\f\v]'))
s_character = DfaRegexp('#\\\\(newline|tab|space|return|[^ \r\n\t\f\v])')
t_character = Token(s_character) >> make_char

s_boolean = (Literal('#f') | Literal('#t'))
t_boolean = Token(s_boolean) >> to_bool

# s_string = String()
s_string = DfaRegexp(r'"[^"\\]*(\\.[^"\\]*)*"')
t_string = Token(s_string)

s_number = Float()
t_number = Token(s_number) >> float_or_int

# s_special_initial = DfaRegexp('[!\\$%&\\*/:<=>\\?\\^_~]')
# s_letter = Letter()
# s_initial = s_letter | s_special_initial
# s_peculiar_identifier = Literal('+') | Literal('-') | Literal('...')
# s_special_subsequent = DfaRegexp('[\\+\\.@\\-]')
# s_digit = Digit()
# s_subsequent = s_initial | s_digit | s_special_subsequent
# s_identifier = Word(s_initial, s_subsequent) | s_peculiar_identifier
ch_initial = 'a-zA-Z!\\$%&\\*/:<=>\\?\\^_~'
ch_digit = '0-9'
ch_special_subsequent = '\\+\\.@\\-'
ch_subsequent = ''.join([ch_initial, ch_digit, ch_special_subsequent])

s_identifier = DfaRegexp('(\\+|\\-|\\.\\.\\.|[%s][%s]*)' % (ch_initial, ch_subsequent))
t_identifier = Token(s_identifier)

s_datum = Delayed()
s_abbrev_prefix = Literal("'") | Literal("`") | Literal(",") | Literal(",@")
t_abbrev_prefix = Token(s_abbrev_prefix)
s_abbreviation = t_abbrev_prefix & s_datum

t_lparen = Token(Literal('('))
t_rparen = Token(Literal(')'))
t_lbrack = Token(Literal('['))
t_rbrack = Token(Literal(']'))
t_dot = Token(Literal('.'))

s_list = Or(
    (~t_lparen & s_datum[:] & ~t_rparen) > List,
    (~t_lparen & (s_datum[1:] & ~t_dot & s_datum & ~t_rparen) > DotList),
    (~t_lbrack & s_datum[:] & ~t_rbrack) > List,
    (~t_lbrack & (s_datum[1:] & ~t_dot & s_datum & ~t_rbrack) > DotList),
    s_abbreviation)
s_compound_datum = s_list # | s_vector
s_symbol = t_identifier > Symbol
s_simple_datum = t_boolean | t_number | t_character | t_string | s_symbol
s_datum += (s_simple_datum | s_compound_datum)

parser = s_datum.string_parser()

parser = s_datum.string_parser()

def parse(s):
    p = parser(s)
    if p is not None:
        return p[0]
    else:
        raise Exception("Cannot parse '%s'" % s)
