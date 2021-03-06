#!/usr/bin/env python3
import sys, time
from parser import Symbol as S, List as L, Char as C
from compiler import compile_and_run

TESTS = [
("integers",
 (("0", 0, "0"),
  ("1", 1, "1"),
  ("-1", -1, "-1"),
  ("10", 10, "10"),
  ("-10", -10, "-10"),
  ("2736", 2736, "2736"),
  ("-2736", -2736, "-2736"),
  ("536870911", 536870911, "536870911"),
  ("-536870912", -536870912, "-536870912"),
  )),

("immediate constants",
 (("#f", False, "#f"),
  ("#t", True, "#t"),
  ("()", L(), "()"),
  ("#\\tab", C("\t"), "#\\tab"),
  ("#\\newline", C("\n"), "#\\newline"),
  ("#\\return", C("\r"), "#\\return"),
  ("#\\space", C(" "), "#\\space"),
  ("#\\!", C("!"), "#\\!"),
  ('#\\"', C('"'), '#\\"'),
  ("#\\#", C("#"), "#\\#"),
  ("#\\$", C("$"), "#\\$"),
  ("#\\%", C("%"), "#\\%"),
  ("#\\&", C("&"), "#\\&"),
  ("#\\'", C("'"), "#\\'"),
  ("#\\(", C("("), "#\\("),
  ("#\\)", C(")"), "#\\)"),
  ("#\\*", C("*"), "#\\*"),
  ("#\\+", C("+"), "#\\+"),
  ("#\\,", C(","), "#\\,"),
  ("#\\-", C("-"), "#\\-"),
  ("#\\.", C("."), "#\\."),
  ("#\\/", C("/"), "#\\/"),
  ("#\\0", C("0"), "#\\0"),
  # ("#\\1", C("1"), "#\\1"),
  # ("#\\2", C("2"), "#\\2"),
  # ("#\\3", C("3"), "#\\3"),
  # ("#\\4", C("4"), "#\\4"),
  # ("#\\5", C("5"), "#\\5"),
  # ("#\\6", C("6"), "#\\6"),
  # ("#\\7", C("7"), "#\\7"),
  # ("#\\8", C("8"), "#\\8"),
  # ("#\\9", C("9"), "#\\9"),
  ("#\\:", C(":"), "#\\:"),
  ("#\\;", C(";"), "#\\;"),
  ("#\\<", C("<"), "#\\<"),
  ("#\\=", C("="), "#\\="),
  ("#\\>", C(">"), "#\\>"),
  ("#\\?", C("?"), "#\\?"),
  ("#\\@", C("@"), "#\\@"),
  ("#\\A", C("A"), "#\\A"),
  # ("#\\B", C("B"), "#\\B"),
  # ("#\\C", C("C"), "#\\C"),
  # ("#\\D", C("D"), "#\\D"),
  # ("#\\E", C("E"), "#\\E"),
  # ("#\\F", C("F"), "#\\F"),
  # ("#\\G", C("G"), "#\\G"),
  # ("#\\H", C("H"), "#\\H"),
  # ("#\\I", C("I"), "#\\I"),
  # ("#\\J", C("J"), "#\\J"),
  # ("#\\K", C("K"), "#\\K"),
  # ("#\\L", C("L"), "#\\L"),
  # ("#\\M", C("M"), "#\\M"),
  # ("#\\N", C("N"), "#\\N"),
  # ("#\\O", C("O"), "#\\O"),
  # ("#\\P", C("P"), "#\\P"),
  # ("#\\Q", C("Q"), "#\\Q"),
  # ("#\\R", C("R"), "#\\R"),
  # ("#\\S", C("S"), "#\\S"),
  # ("#\\T", C("T"), "#\\T"),
  # ("#\\U", C("U"), "#\\U"),
  # ("#\\V", C("V"), "#\\V"),
  # ("#\\W", C("W"), "#\\W"),
  # ("#\\X", C("X"), "#\\X"),
  # ("#\\Y", C("Y"), "#\\Y"),
  # ("#\\Z", C("Z"), "#\\Z"),
  ("#\\[", C("["), "#\\["),
  ("#\\\\", C("\\"), "#\\\\"),
  ("#\\]", C("]"), "#\\]"),
  ("#\\^", C("^"), "#\\^"),
  ("#\\_", C("_"), "#\\_"),
  ("#\\`", C("`"), "#\\`"),
  ("#\\a", C("a"), "#\\a"),
  # ("#\\b", C("b"), "#\\b"),
  # ("#\\c", C("c"), "#\\c"),
  # ("#\\d", C("d"), "#\\d"),
  # ("#\\e", C("e"), "#\\e"),
  # ("#\\f", C("f"), "#\\f"),
  # ("#\\g", C("g"), "#\\g"),
  # ("#\\h", C("h"), "#\\h"),
  # ("#\\i", C("i"), "#\\i"),
  # ("#\\j", C("j"), "#\\j"),
  # ("#\\k", C("k"), "#\\k"),
  # ("#\\l", C("l"), "#\\l"),
  # ("#\\m", C("m"), "#\\m"),
  # ("#\\n", C("n"), "#\\n"),
  # ("#\\o", C("o"), "#\\o"),
  # ("#\\p", C("p"), "#\\p"),
  # ("#\\q", C("q"), "#\\q"),
  # ("#\\r", C("r"), "#\\r"),
  # ("#\\s", C("s"), "#\\s"),
  # ("#\\t", C("t"), "#\\t"),
  # ("#\\u", C("u"), "#\\u"),
  # ("#\\v", C("v"), "#\\v"),
  # ("#\\w", C("w"), "#\\w"),
  # ("#\\x", C("x"), "#\\x"),
  # ("#\\y", C("y"), "#\\y"),
  # ("#\\z", C("z"), "#\\z"),
  ("#\\{", C("{"), "#\\{"),
  ("#\\|", C("|"), "#\\|"),
  ("#\\}", C("}"), "#\\}"),
  ("#\\~", C("~"), "#\\~"),
  )),

("$fxadd1",
 (("($fxadd1 0)", L(S("$fxadd1"), 0), "1"),
  ("($fxadd1 -1)", L(S("$fxadd1"), -1), "0"),
  ("($fxadd1 1)", L(S("$fxadd1"), 1), "2"),
  ("($fxadd1 -100)", L(S("$fxadd1"), -100), "-99"),
  ("($fxadd1 1000)", L(S("$fxadd1"), 1000), "1001"),
  ("($fxadd1 536870910)", L(S("$fxadd1"), 536870910), "536870911"),
  ("($fxadd1 -536870912)", L(S("$fxadd1"), -536870912), "-536870911"),
  ("($fxadd1 ($fxadd1 0))", L(S("$fxadd1"), L(S("$fxadd1"), 0)), "2"),
  ("($fxadd1 ($fxadd1 ($fxadd1 ($fxadd1 ($fxadd1 ($fxadd1 12))))))", L(S("$fxadd1"), L(S("$fxadd1"), L(S("$fxadd1"), L(S("$fxadd1"), L(S("$fxadd1"), L(S("$fxadd1"), 12)))))), "18"),
  )),

("$fixnum->char and $char->fixnum",
 (("($fixnum->char 65)", L(S("$fixnum->char"), 65), "#\\A"),
  ("($fixnum->char 97)", L(S("$fixnum->char"), 97), "#\\a"),
  ("($fixnum->char 122)", L(S("$fixnum->char"), 122), "#\\z"),
  ("($fixnum->char 90)", L(S("$fixnum->char"), 90), "#\\Z"),
  ("($fixnum->char 48)", L(S("$fixnum->char"), 48), "#\\0"),
  ("($fixnum->char 57)", L(S("$fixnum->char"), 57), "#\\9"),
  ("($char->fixnum #\\A)", L(S("$char->fixnum"), C("A")), "65"),
  ("($char->fixnum #\\a)", L(S("$char->fixnum"), C("a")), "97"),
  ("($char->fixnum #\\z)", L(S("$char->fixnum"), C("z")), "122"),
  ("($char->fixnum #\\Z)", L(S("$char->fixnum"), C("Z")), "90"),
  ("($char->fixnum #\\0)", L(S("$char->fixnum"), C("0")), "48"),
  ("($char->fixnum #\\9)", L(S("$char->fixnum"), C("9")), "57"),
  ("($char->fixnum ($fixnum->char 12))", L(S("$char->fixnum"), L(S("$fixnum->char"), 12)), "12"),
  ("($fixnum->char ($char->fixnum #\\x))", L(S("$fixnum->char"), L(S("$char->fixnum"), C("x"))), "#\\x"),
  )),

("fixnum?",
 (("(fixnum? 0)", L(S("fixnum?"), 0), "#t"),
  ("(fixnum? 1)", L(S("fixnum?"), 1), "#t"),
  ("(fixnum? -1)", L(S("fixnum?"), -1), "#t"),
  ("(fixnum? 37287)", L(S("fixnum?"), 37287), "#t"),
  ("(fixnum? -23873)", L(S("fixnum?"), -23873), "#t"),
  ("(fixnum? 536870911)", L(S("fixnum?"), 536870911), "#t"),
  ("(fixnum? -536870912)", L(S("fixnum?"), -536870912), "#t"),
  ("(fixnum? #t)", L(S("fixnum?"), True), "#f"),
  ("(fixnum? #f)", L(S("fixnum?"), False), "#f"),
  ("(fixnum? ())", L(S("fixnum?"), L()), "#f"),
  ("(fixnum? #\\Q)", L(S("fixnum?"), C("Q")), "#f"),
  ("(fixnum? (fixnum? 12))", L(S("fixnum?"), L(S("fixnum?"), 12)), "#f"),
  ("(fixnum? (fixnum? #f))", L(S("fixnum?"), L(S("fixnum?"), False)), "#f"),
  ("(fixnum? (fixnum? #\\A))", L(S("fixnum?"), L(S("fixnum?"), C("A"))), "#f"),
  ("(fixnum? ($char->fixnum #\\r))", L(S("fixnum?"), L(S("$char->fixnum"), C("r"))), "#t"),
  ("(fixnum? ($fixnum->char 12))", L(S("fixnum?"), L(S("$fixnum->char"), 12)), "#f"),
  )),

("$fxzero?",
 (("($fxzero? 0)", L(S("$fxzero?"), 0), "#t"),
  ("($fxzero? 1)", L(S("$fxzero?"), 1), "#f"),
  ("($fxzero? -1)", L(S("$fxzero?"), -1), "#f"),
  )),

("null?",
 (("(null? ())", L(S("null?"), L()), "#t"),
  ("(null? #f)", L(S("null?"), False), "#f"),
  ("(null? #t)", L(S("null?"), True), "#f"),
  ("(null? (null? ()))", L(S("null?"), L(S("null?"), L())), "#f"),
  ("(null? #\\a)", L(S("null?"), C("a")), "#f"),
  ("(null? 0)", L(S("null?"), 0), "#f"),
  ("(null? -10)", L(S("null?"), -10), "#f"),
  ("(null? 10)", L(S("null?"), 10), "#f"),
  )),

("boolean?",
 (("(boolean? #t)", L(S("boolean?"), True), "#t"),
  ("(boolean? #f)", L(S("boolean?"), False), "#t"),
  ("(boolean? 0)", L(S("boolean?"), 0), "#f"),
  ("(boolean? 1)", L(S("boolean?"), 1), "#f"),
  ("(boolean? -1)", L(S("boolean?"), -1), "#f"),
  ("(boolean? ())", L(S("boolean?"), L()), "#f"),
  ("(boolean? #\\a)", L(S("boolean?"), C("a")), "#f"),
  ("(boolean? (boolean? 0))", L(S("boolean?"), L(S("boolean?"), 0)), "#t"),
  ("(boolean? (fixnum? (boolean? 0)))", L(S("boolean?"), L(S("fixnum?"), L(S("boolean?"), 0))), "#t"),
  )),

("char?",
 (("(char? #\\a)", L(S("char?"), C("a")), "#t"),
  ("(char? #\\Z)", L(S("char?"), C("Z")), "#t"),
  ("(char? #\\newline)", L(S("char?"), C("\n")), "#t"),
  ("(char? #t)", L(S("char?"), True), "#f"),
  ("(char? #f)", L(S("char?"), False), "#f"),
  ("(char? ())", L(S("char?"), L()), "#f"),
  ("(char? (char? #t))", L(S("char?"), L(S("char?"), True)), "#f"),
  ("(char? 0)", L(S("char?"), 0), "#f"),
  ("(char? 23870)", L(S("char?"), 23870), "#f"),
  ("(char? -23789)", L(S("char?"), -23789), "#f"),
  )),

("not",
 (("(not #t)", L(S("not"), True), "#f"),
  ("(not #f)", L(S("not"), False), "#t"),
  ("(not 15)", L(S("not"), 15), "#f"),
  ("(not ())", L(S("not"), L()), "#f"),
  ("(not #\\A)", L(S("not"), C("A")), "#f"),
  ("(not (not #t))", L(S("not"), L(S("not"), True)), "#t"),
  ("(not (not #f))", L(S("not"), L(S("not"), False)), "#f"),
  ("(not (not 15))", L(S("not"), L(S("not"), 15)), "#t"),
  ("(not (fixnum? 15))", L(S("not"), L(S("fixnum?"), 15)), "#f"),
  ("(not (fixnum? #f))", L(S("not"), L(S("fixnum?"), False)), "#t"),
  )),

("$fxlognot",
 (
  ("($fxlognot 0)", L(S("$fxlognot"), 0), "-1"),
  ("($fxlognot -1)", L(S("$fxlognot"), -1), "0"),
  ("($fxlognot 1)", L(S("$fxlognot"), 1), "-2"),
  ("($fxlognot -2)", L(S("$fxlognot"), -2), "1"),
  ("($fxlognot 536870911)", L(S("$fxlognot"), 536870911), "-536870912"),
  ("($fxlognot -536870912)", L(S("$fxlognot"), -536870912), "536870911"),
  ("($fxlognot ($fxlognot 237463))", L(S("$fxlognot"), L(S("$fxlognot"), 237463)), "237463"),
  )),

("and",
 (("(and)", L(S("and")), "#t"),
  ("(and #t)", L(S("and"), True), "#t"),
  ("(and #f)", L(S("and"), False), "#f"),
  ("(and #t #t #t)", L(S("and"), True, True, True), "#t"),
  ("(and #t #t #f)", L(S("and"), True, True, False), "#f"),
  ("(and #t #f #t)", L(S("and"), True, False, True), "#f"),
  ("(and (not (char? 1)) (not (boolean? 2)) (not (not (boolean? #t))))", L(S("and"), L(S("not"), L(S("char?"), 1)), L(S("not"), L(S("boolean?"), 2)), L(S("not"), L(S("not"), L(S("boolean?"), True)))), "#t"),
  ("(and (not (char? #\\a)) (not (boolean? 2)) (not (not (boolean? #t))))", L(S("and"), L(S("not"), L(S("char?"), C("a"))), L(S("not"), L(S("boolean?"), 2)), L(S("not"), L(S("not"), L(S("boolean?"), True)))), "#f"),
  ("(and (not (char? 1)) (not (boolean? #t)) (not (not (boolean? #t))))", L(S("and"), L(S("not"), L(S("char?"), 1)), L(S("not"), L(S("boolean?"), True)), L(S("not"), L(S("not"), L(S("boolean?"), True)))), "#f"),
  ("(and (not (char? 1)) (not (boolean? 2)) (not (not (boolean? 2))))", L(S("and"), L(S("not"), L(S("char?"), 1)), L(S("not"), L(S("boolean?"), 2)), L(S("not"), L(S("not"), L(S("boolean?"), 2)))), "#f"),
  )),

("if",
 (("(if #t 12 13)", L(S("if"), True, 12, 13), "12"),
  ("(if #f 12 13)", L(S("if"), False, 12, 13), "13"),
  ("(if 0 12 13) ", L(S("if"), 0, 12, 13), "12"),
  ("(if () 43 ())", L(S("if"), L(), 43, L()), "43"),
  ("(if #t (if 12 13 4) 17)", L(S("if"), True, L(S("if"), 12, 13, 4), 17), "13"),
  ("(if #f 12 (if #f 13 4))", L(S("if"), False, 12, (L(S("if"), False, 13, 4))), "4"),
  ("(if #\\X (if 1 2 3) (if 4 5 6))", L(S("if"), C("X"), L(S("if"), 1, 2, 3), L(S("if"), 4, 5, 6)), "2"),
  ("(if (not (boolean? #t)) 15 (boolean? #f))", L(S("if"), L(S("not"), L(S("boolean?"), True)), 15, L(S("boolean?"), False)), "#t"),

  ("(if (if (char? #\\a) (boolean? #\\b) (fixnum? #\\c)) 119 -23)", L(S("if"), L(S("if"), L(S("char?"), C("a")), L(S("boolean?"), C("b")), L(S("fixnum?"), C("c"))), 119, -23), "-23"),
  ("(if (if (if (not 1) (not 2) (not 3)) 4 5) 6 7)", L(S("if"), L(S("if"), L(S("if"), L(S("not"), 1), L(S("not"), 2), L(S("not"), 3)), 4, 5), 6, 7), "6"),
  ("(if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7)", L(S("if"), L(S("not"), L(S("if"), L(S("if"), L(S("not"), 1), L(S("not"), 2), L(S("not"), 3)), 4, 5)), 6, 7), "7"),
  ("(not (if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7))", L(S("not"), L(S("if"), L(S("not"), L(S("if"), L(S("if"), L(S("not"), 1), L(S("not"), 2), L(S("not"), 3)), 4, 5)), 6, 7)), "#f"),
  ("(if (char? 12) 13 14)", L(S("if"), L(S("char?"), 12), 13, 14), "14"),
  ("(if (char? #\\a) 13 14)", L(S("if"), L(S("char?"), C("a")), 13, 14), "13"),
  ("($fxadd1 (if ($fxsub1 1) ($fxsub1 13) 14))", L(S("$fxadd1"), L(S("if"), L(S("$fxsub1"), 1), L(S("$fxsub1"), 13), 14)), "13"),
  )),

("fx+",
 (("(fx+ 1 2)", L(S("fx+"), 1, 2),  "3"),
  ("(fx+ 1 -2)", L(S("fx+"), 1, -2),  "-1"),
  ("(fx+ -1 2)", L(S("fx+"), -1, 2),  "1"),
  ("(fx+ -1 -2)", L(S("fx+"), -1, -2),  "-3"),
  ("(fx+ 536870911 -1)", L(S("fx+"), 536870911, -1),  "536870910"),
  ("(fx+ 536870910 1)", L(S("fx+"), 536870910, 1),  "536870911"),
  ("(fx+ -536870912 1)", L(S("fx+"), -536870912, 1),  "-536870911"),
  ("(fx+ -536870911 -1)", L(S("fx+"), -536870911, -1),  "-536870912"),
  ("(fx+ 536870911 -536870912)", L(S("fx+"), 536870911, -536870912),  "-1"),
  ("(fx+ 1 (fx+ 2 3))", L(S("fx+"), 1, L(S("fx+"), 2, 3)),  "6"),
  ("(fx+ 1 (fx+ 2 -3))", L(S("fx+"), 1, L(S("fx+"), 2, -3)),  "0"),
  ("(fx+ 1 (fx+ -2 3))", L(S("fx+"), 1, L(S("fx+"), -2, 3)),  "2"),
  ("(fx+ 1 (fx+ -2 -3))", L(S("fx+"), 1, L(S("fx+"), -2, -3)),  "-4"),
  ("(fx+ -1 (fx+ 2 3))", L(S("fx+"), -1, L(S("fx+"), 2, 3)),  "4"),
  ("(fx+ -1 (fx+ 2 -3))", L(S("fx+"), -1, L(S("fx+"), 2, -3)),  "-2"),
  ("(fx+ -1 (fx+ -2 3))", L(S("fx+"), -1, L(S("fx+"), -2, 3)),  "0"),
  ("(fx+ -1 (fx+ -2 -3))", L(S("fx+"), -1, L(S("fx+"), -2, -3)),  "-6"),
  ("(fx+ (fx+ 1 2) 3)", L(S("fx+"), L(S("fx+"), 1, 2), 3),  "6"),
  ("(fx+ (fx+ 1 2) -3)", L(S("fx+"), L(S("fx+"), 1, 2), -3),  "0"),
  ("(fx+ (fx+ 1 -2) 3)", L(S("fx+"), L(S("fx+"), 1, -2), 3),  "2"),
  ("(fx+ (fx+ 1 -2) -3)", L(S("fx+"), L(S("fx+"), 1, -2), -3),  "-4"),
  ("(fx+ (fx+ -1 2) 3)", L(S("fx+"), L(S("fx+"), -1, 2), 3),  "4"),
  ("(fx+ (fx+ -1 2) -3)", L(S("fx+"), L(S("fx+"), -1, 2), -3),  "-2"),
  ("(fx+ (fx+ -1 -2) 3)", L(S("fx+"), L(S("fx+"), -1, -2), 3),  "0"),
  ("(fx+ (fx+ -1 -2) -3)", L(S("fx+"), L(S("fx+"), -1, -2), -3),  "-6"),
  ("(fx+ (fx+ (fx+ (fx+ (fx+ (fx+ (fx+ (fx+ 1 2) 3) 4) 5) 6) 7) 8) 9)", L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), 1, 2), 3), 4), 5), 6), 7), 8), 9),  "45"),
  ("(fx+ 1 (fx+ 2 (fx+ 3 (fx+ 4 (fx+ 5 (fx+ 6 (fx+ 7 (fx+ 8 9))))))))", L(S("fx+"), 1, L(S("fx+"), 2, L(S("fx+"), 3, L(S("fx+"), 4, L(S("fx+"), 5, L(S("fx+"), 6, L(S("fx+"), 7, L(S("fx+"), 8, 9)))))))),  "45"),
  )),

("fx-",
 (
  ("(fx- 1 2)", L(S("fx-"), 1, 2), "-1"),
  ("(fx- 1 -2)", L(S("fx-"), 1, -2), "3"),
  ("(fx- -1 2)", L(S("fx-"), -1, 2), "-3"),
  ("(fx- -1 -2)", L(S("fx-"), -1, -2), "1"),
  ("(fx- 536870910 -1)", L(S("fx-"), 536870910, -1), "536870911"),
  ("(fx- 536870911 1)", L(S("fx-"), 536870911, 1), "536870910"),
  ("(fx- -536870911 1)", L(S("fx-"), -536870911, 1), "-536870912"),
  ("(fx- -536870912 -1)", L(S("fx-"), -536870912, -1), "-536870911"),
  ("(fx- 1 536870911)", L(S("fx-"), 1, 536870911), "-536870910"),
  ("(fx- -1 536870911)", L(S("fx-"), -1, 536870911), "-536870912"),
  ("(fx- 1 -536870910)", L(S("fx-"), 1, -536870910), "536870911"),
  ("(fx- -1 -536870912)", L(S("fx-"), -1, -536870912), "536870911"),
  ("(fx- 536870911 536870911)", L(S("fx-"), 536870911, 536870911), "0"),
  # ("(fx- 536870911 -536870912)", L(S("fx-"), 536870911, -536870912), "-1"),
  ("(fx- -536870911 -536870912)", L(S("fx-"), -536870911, -536870912), "1"),
  ("(fx- 1 (fx- 2 3))", L(S("fx-"), 1, L(S("fx-"), 2, 3)), "2"),
  ("(fx- 1 (fx- 2 -3))", L(S("fx-"), 1, L(S("fx-"), 2, -3)), "-4"),
  ("(fx- 1 (fx- -2 3))", L(S("fx-"), 1, L(S("fx-"), -2, 3)), "6"),
  ("(fx- 1 (fx- -2 -3))", L(S("fx-"), 1, L(S("fx-"), -2, -3)), "0"),
  ("(fx- -1 (fx- 2 3))", L(S("fx-"), -1, L(S("fx-"), 2, 3)), "0"),
  ("(fx- -1 (fx- 2 -3))", L(S("fx-"), -1, L(S("fx-"), 2, -3)), "-6"),
  ("(fx- -1 (fx- -2 3))", L(S("fx-"), -1, L(S("fx-"), -2, 3)), "4"),
  ("(fx- -1 (fx- -2 -3))", L(S("fx-"), -1, L(S("fx-"), -2, -3)), "-2"),
  ("(fx- 0 (fx- -2 -3))", L(S("fx-"), 0, L(S("fx-"), -2, -3)), "-1"),
  ("(fx- (fx- 1 2) 3)", L(S("fx-"), L(S("fx-"), 1, 2), 3), "-4"),
  ("(fx- (fx- 1 2) -3)", L(S("fx-"), L(S("fx-"), 1, 2), -3), "2"),
  ("(fx- (fx- 1 -2) 3)", L(S("fx-"), L(S("fx-"), 1, -2), 3), "0"),
  ("(fx- (fx- 1 -2) -3)", L(S("fx-"), L(S("fx-"), 1, -2), -3), "6"),
  ("(fx- (fx- -1 2) 3)", L(S("fx-"), L(S("fx-"), -1, 2), 3), "-6"),
  ("(fx- (fx- -1 2) -3)", L(S("fx-"), L(S("fx-"), -1, 2), -3), "0"),
  ("(fx- (fx- -1 -2) 3)", L(S("fx-"), L(S("fx-"), -1, -2), 3), "-2"),
  ("(fx- (fx- -1 -2) -3)", L(S("fx-"), L(S("fx-"), -1, -2), -3), "4"),
  ("(fx- (fx- (fx- (fx- (fx- (fx- (fx- (fx- 1 2) 3) 4) 5) 6) 7) 8) 9)", L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), 1, 2), 3), 4), 5), 6), 7), 8), 9), "-43"),
  ("(fx- 1 (fx- 2 (fx- 3 (fx- 4 (fx- 5 (fx- 6 (fx- 7 (fx- 8 9))))))))", L(S("fx-"), 1, L(S("fx-"), 2, L(S("fx-"), 3, L(S("fx-"), 4, L(S("fx-"), 5, L(S("fx-"), 6, L(S("fx-"), 7, L(S("fx-"), 8, 9)))))))), "5"),
  )),

("fx*",
 (
  ("(fx* 2 3)", L(S("fx*"), 2, 3), "6"),
  ("(fx* 2 -3)", L(S("fx*"), 2, -3), "-6"),
  ("(fx* -2 3)", L(S("fx*"), -2, 3), "-6"),
  ("(fx* -2 -3)", L(S("fx*"), -2, -3), "6"),
  ("(fx* 536870911 1)", L(S("fx*"), 536870911, 1), "536870911"),
  ("(fx* 536870911 -1)", L(S("fx*"), 536870911, -1), "-536870911"),
  ("(fx* -536870912 1)", L(S("fx*"), -536870912, 1), "-536870912"),
  ("(fx* -536870911 -1)", L(S("fx*"), -536870911, -1), "536870911"),
  ("(fx* 2 (fx* 3 4))", L(S("fx*"), 2, L(S("fx*"), 3, 4)), "24"),
  ("(fx* (fx* 2 3) 4)", L(S("fx*"), L(S("fx*"), 2, 3), 4), "24"),
  ("(fx* (fx* (fx* (fx* (fx* 2 3) 4) 5) 6) 7)", L(S("fx*"), L(S("fx*"), L(S("fx*"), L(S("fx*"), L(S("fx*"), 2, 3), 4), 5), 6), 7), "5040"),
  ("(fx* 2 (fx* 3 (fx* 4 (fx* 5 (fx* 6 7)))))", L(S("fx*"), 2, L(S("fx*"), 3, L(S("fx*"), 4, L(S("fx*"), 5, L(S("fx*"), 6, 7))))), "5040"),
  )),

("fxlogand and fxlogor",
 (
  ("(fxlogor 3 16)", L(S("fxlogor"), 3, 16), "19"),
  ("(fxlogor 3 5)", L(S("fxlogor"), 3, 5), "7"),
  ("(fxlogor 3 7)", L(S("fxlogor"), 3, 7), "7"),
  ("(fxlognot (fxlogor (fxlognot 7) 1))", L(S("fxlognot"), L(S("fxlogor"), L(S("fxlognot"), 7), 1)), "6"),
  ("(fxlognot (fxlogor 1 (fxlognot 7)))", L(S("fxlognot"), L(S("fxlogor"), 1, L(S("fxlognot"), 7))), "6"),
  ("(fxlogand 3 7)", L(S("fxlogand"), 3, 7), "3"),
  ("(fxlogand 3 5)", L(S("fxlogand"), 3, 5), "1"),
  ("(fxlogand 2346 (fxlognot 2346))", L(S("fxlogand"), 2346, L(S("fxlognot"), 2346)), "0"),
  ("(fxlogand (fxlognot 2346) 2346)", L(S("fxlogand"), L(S("fxlognot"), 2346), 2346), "0"),
  ("(fxlogand 2376 2376)", L(S("fxlogand"), 2376, 2376), "2376"),
  )),

("fx=",
 (
  ("(fx= 12 13)", L(S("fx="), 12, 13), "#f"),
  ("(fx= 12 12)", L(S("fx="), 12, 12), "#t"),
  ("(fx= 16 (fx+ 13 3))", L(S("fx="), 16, L(S("fx+"), 13, 3)), "#t"),
  ("(fx= 16 (fx+ 13 13))", L(S("fx="), 16, L(S("fx+"), 13, 13)), "#f"),
  ("(fx= (fx+ 13 3) 16)", L(S("fx="), L(S("fx+"), 13, 3), 16), "#t"),
  ("(fx= (fx+ 13 13) 16)", L(S("fx="), L(S("fx+"), 13, 13), 16), "#f"),
  )),

("fx<",
 (
  ("(fx< 12 13)", L(S("fx<"), 12, 13), "#t"),
  ("(fx< 12 12)", L(S("fx<"), 12, 12), "#f"),
  ("(fx< 13 12)", L(S("fx<"), 13, 12), "#f"),
  ("(fx< 16 (fx+ 13 1))", L(S("fx<"), 16, L(S("fx+"), 13, 1)), "#f"),
  ("(fx< 16 (fx+ 13 3))", L(S("fx<"), 16, L(S("fx+"), 13, 3)), "#f"),
  ("(fx< 16 (fx+ 13 13))", L(S("fx<"), 16, L(S("fx+"), 13, 13)), "#t"),
  ("(fx< (fx+ 13 1) 16)", L(S("fx<"), L(S("fx+"), 13, 1), 16), "#t"),
  ("(fx< (fx+ 13 3) 16)", L(S("fx<"), L(S("fx+"), 13, 3), 16), "#f"),
  ("(fx< (fx+ 13 13) 16)", L(S("fx<"), L(S("fx+"), 13, 13), 16), "#f"),
  )),

("fx<=",
 (
  ("(fx<= 12 13)", L(S("fx<="), 12, 13), "#t"),
  ("(fx<= 12 12)", L(S("fx<="), 12, 12), "#t"),
  ("(fx<= 13 12)", L(S("fx<="), 13, 12), "#f"),
  ("(fx<= 16 (fx+ 13 1))", L(S("fx<="), 16, L(S("fx+"), 13, 1)), "#f"),
  ("(fx<= 16 (fx+ 13 3))", L(S("fx<="), 16, L(S("fx+"), 13, 3)), "#t"),
  ("(fx<= 16 (fx+ 13 13))", L(S("fx<="), 16, L(S("fx+"), 13, 13)), "#t"),
  ("(fx<= (fx+ 13 1) 16)", L(S("fx<="), L(S("fx+"), 13, 1), 16), "#t"),
  ("(fx<= (fx+ 13 3) 16)", L(S("fx<="), L(S("fx+"), 13, 3), 16), "#t"),
  ("(fx<= (fx+ 13 13) 16)", L(S("fx<="), L(S("fx+"), 13, 13), 16), "#f"),
  )),

("fx>",
 (
  ("(fx> 12 13)", L(S("fx>"), 12, 13), "#f"),
  ("(fx> 12 12)", L(S("fx>"), 12, 12), "#f"),
  ("(fx> 13 12)", L(S("fx>"), 13, 12), "#t"),
  ("(fx> 16 (fx+ 13 1))", L(S("fx>"), 16, L(S("fx+"), 13, 1)), "#t"),
  ("(fx> 16 (fx+ 13 3))", L(S("fx>"), 16, L(S("fx+"), 13, 3)), "#f"),
  ("(fx> 16 (fx+ 13 13))", L(S("fx>"), 16, L(S("fx+"), 13, 13)), "#f"),
  ("(fx> (fx+ 13 1) 16)", L(S("fx>"), L(S("fx+"), 13, 1), 16), "#f"),
  ("(fx> (fx+ 13 3) 16)", L(S("fx>"), L(S("fx+"), 13, 3), 16), "#f"),
  ("(fx> (fx+ 13 13) 16)", L(S("fx>"), L(S("fx+"), 13, 13), 16), "#t"),
  )),

("fx>=",
 (
  ("(fx>= 12 13)", L(S("fx>="), 12, 13), "#f"),
  ("(fx>= 12 12)", L(S("fx>="), 12, 12), "#t"),
  ("(fx>= 13 12)", L(S("fx>="), 13, 12), "#t"),
  ("(fx>= 16 (fx+ 13 1))", L(S("fx>="), 16, L(S("fx+"), 13, 1)), "#t"),
  ("(fx>= 16 (fx+ 13 3))", L(S("fx>="), 16, L(S("fx+"), 13, 3)), "#t"),
  ("(fx>= 16 (fx+ 13 13))", L(S("fx>="), 16, L(S("fx+"), 13, 13)), "#f"),
  ("(fx>= (fx+ 13 1) 16)", L(S("fx>="), L(S("fx+"), 13, 1), 16), "#f"),
  ("(fx>= (fx+ 13 3) 16)", L(S("fx>="), L(S("fx+"), 13, 3), 16), "#t"),
  ("(fx>= (fx+ 13 13) 16)", L(S("fx>="), L(S("fx+"), 13, 13), 16), "#t"),
  )),


("if",
 (
  ("(if (fx= 12 13) 12 13)", L(S("if"), L(S("fx="), 12, 13), 12, 13), "13"),
  ("(if (fx= 12 12) 13 14)", L(S("if"), L(S("fx="), 12, 12), 13, 14), "13"),
  ("(if (fx< 12 13) 12 13)", L(S("if"), L(S("fx<"), 12, 13), 12, 13), "12"),
  ("(if (fx< 12 12) 13 14)", L(S("if"), L(S("fx<"), 12, 12), 13, 14), "14"),
  ("(if (fx< 13 12) 13 14)", L(S("if"), L(S("fx<"), 13, 12), 13, 14), "14"),
  ("(if (fx<= 12 13) 12 13)", L(S("if"), L(S("fx<="), 12, 13), 12, 13), "12"),
  ("(if (fx<= 12 12) 12 13)", L(S("if"), L(S("fx<="), 12, 12), 12, 13), "12"),
  ("(if (fx<= 13 12) 13 14)", L(S("if"), L(S("fx<="), 13, 12), 13, 14), "14"),
  ("(if (fx> 12 13) 12 13)", L(S("if"), L(S("fx>"), 12, 13), 12, 13), "13"),
  ("(if (fx> 12 12) 12 13)", L(S("if"), L(S("fx>"), 12, 12), 12, 13), "13"),
  ("(if (fx> 13 12) 13 14)", L(S("if"), L(S("fx>"), 13, 12), 13, 14), "13"),
  ("(if (fx>= 12 13) 12 13)", L(S("if"), L(S("fx>="), 12, 13), 12, 13), "13"),
  ("(if (fx>= 12 12) 12 13)", L(S("if"), L(S("fx>="), 12, 12), 12, 13), "12"),
  ("(if (fx>= 13 12) 13 14)", L(S("if"), L(S("fx>="), 13, 12), 13, 14), "13"),
  )),

("binary primitives",
 (("(fxlognot -7)", L(S("fxlognot"), -7), "6"),
  ("(fxlognot (fxlogor (fxlognot 7) 1))", L(S("fxlognot"), L(S("fxlogor"), L(S("fxlognot"), 7), 1)), "6"),
  ("(fxlognot (fxlogor (fxlognot 7) (fxlognot 2)))", L(S("fxlognot"), L(S("fxlogor"), L(S("fxlognot"), 7), L(S("fxlognot"), 2))), "2"),
  ("(fxlogand (fxlognot (fxlognot 12)) (fxlognot (fxlognot 12)))", L(S("fxlogand"), L(S("fxlognot"), L(S("fxlognot"), 12)), L(S("fxlognot"), L(S("fxlognot"), 12))), "12"),
  ("(fx+ (fx+ 1 2) (fx+ 3 4))", L(S("fx+"), L(S("fx+"), 1, 2), L(S("fx+"), 3, 4)), "10"),
  ("(fx+ (fx+ 1 2) (fx+ 3 -4))", L(S("fx+"), L(S("fx+"), 1, 2), L(S("fx+"), 3, -4)), "2"),
  ("(fx+ (fx+ 1 2) (fx+ -3 4))", L(S("fx+"), L(S("fx+"), 1, 2), L(S("fx+"), -3, 4)), "4"),
  ("(fx+ (fx+ 1 2) (fx+ -3 -4))", L(S("fx+"), L(S("fx+"), 1, 2), L(S("fx+"), -3, -4)), "-4"),
  ("(fx+ (fx+ 1 -2) (fx+ 3 4))", L(S("fx+"), L(S("fx+"), 1, -2), L(S("fx+"), 3, 4)), "6"),
  ("(fx+ (fx+ 1 -2) (fx+ 3 -4))", L(S("fx+"), L(S("fx+"), 1, -2), L(S("fx+"), 3, -4)), "-2"),
  ("(fx+ (fx+ 1 -2) (fx+ -3 4))", L(S("fx+"), L(S("fx+"), 1, -2), L(S("fx+"), -3, 4)), "0"),
  ("(fx+ (fx+ 1 -2) (fx+ -3 -4))", L(S("fx+"), L(S("fx+"), 1, -2), L(S("fx+"), -3, -4)), "-8"),
  ("(fx+ (fx+ -1 2) (fx+ 3 4))", L(S("fx+"), L(S("fx+"), -1, 2), L(S("fx+"), 3, 4)), "8"),
  ("(fx+ (fx+ -1 2) (fx+ 3 -4))", L(S("fx+"), L(S("fx+"), -1, 2), L(S("fx+"), 3, -4)), "0"),
  ("(fx+ (fx+ -1 2) (fx+ -3 4))", L(S("fx+"), L(S("fx+"), -1, 2), L(S("fx+"), -3, 4)), "2"),
  ("(fx+ (fx+ -1 2) (fx+ -3 -4))", L(S("fx+"), L(S("fx+"), -1, 2), L(S("fx+"), -3, -4)), "-6"),
  ("(fx+ (fx+ -1 -2) (fx+ 3 4))", L(S("fx+"), L(S("fx+"), -1, -2), L(S("fx+"), 3, 4)), "4"),
  ("(fx+ (fx+ -1 -2) (fx+ 3 -4))", L(S("fx+"), L(S("fx+"), -1, -2), L(S("fx+"), 3, -4)), "-4"),
  ("(fx+ (fx+ -1 -2) (fx+ -3 4))", L(S("fx+"), L(S("fx+"), -1, -2), L(S("fx+"), -3, 4)), "-2"),
  ("(fx+ (fx+ -1 -2) (fx+ -3 -4))", L(S("fx+"), L(S("fx+"), -1, -2), L(S("fx+"), -3, -4)), "-10"),
  ("(fx+ (fx+ (fx+ (fx+ (fx+ (fx+ (fx+ (fx+ 1 2) 3) 4) 5) 6) 7) 8) 9)",
   L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), 1, 2), 3), 4), 5), 6), 7), 8), 9), "45"),
  ("(fx+ 1 (fx+ 2 (fx+ 3 (fx+ 4 (fx+ 5 (fx+ 6 (fx+ 7 (fx+ 8 9))))))))",
   L(S("fx+"), 1, L(S("fx+"), 2, L(S("fx+"), 3, L(S("fx+"), 4, L(S("fx+"), 5, L(S("fx+"), 6, L(S("fx+"), 7, L(S("fx+"), 8, 9)))))))), "45"),
  ("(fx+ (fx+ (fx+ (fx+ 1 2) (fx+ 3 4)) (fx+ (fx+ 5 6) (fx+ 7 8))) (fx+ (fx+ (fx+ 9 10) (fx+ 11 12)) (fx+ (fx+ 13 14) (fx+ 15 16))))",
   L(S("fx+"), L(S("fx+"), L(S("fx+"), L(S("fx+"), 1, 2), L(S("fx+"), 3, 4)), L(S("fx+"), L(S("fx+"), 5, 6), L(S("fx+"), 7, 8))), L(S("fx+"), L(S("fx+"), L(S("fx+"), 9, 10), L(S("fx+"), 11, 12)), L(S("fx+"), L(S("fx+"), 13, 14), L(S("fx+"), 15, 16)))), "136"),
  ("(fx- (fx- 1 2) (fx- 3 4))", L(S("fx-"), L(S("fx-"), 1, 2), L(S("fx-"), 3, 4)), "0"),
  ("(fx- (fx- 1 2) (fx- 3 -4))", L(S("fx-"), L(S("fx-"), 1, 2), L(S("fx-"), 3, -4)), "-8"),
  ("(fx- (fx- 1 2) (fx- -3 4))", L(S("fx-"), L(S("fx-"), 1, 2), L(S("fx-"), -3, 4)), "6"),
  ("(fx- (fx- 1 2) (fx- -3 -4))", L(S("fx-"), L(S("fx-"), 1, 2), L(S("fx-"), -3, -4)), "-2"),
  ("(fx- (fx- 1 -2) (fx- 3 4))", L(S("fx-"), L(S("fx-"), 1, -2), L(S("fx-"), 3, 4)), "4"),
  ("(fx- (fx- 1 -2) (fx- 3 -4))", L(S("fx-"), L(S("fx-"), 1, -2), L(S("fx-"), 3, -4)), "-4"),
  ("(fx- (fx- 1 -2) (fx- -3 4))", L(S("fx-"), L(S("fx-"), 1, -2), L(S("fx-"), -3, 4)), "10"),
  ("(fx- (fx- 1 -2) (fx- -3 -4))", L(S("fx-"), L(S("fx-"), 1, -2), L(S("fx-"), -3, -4)), "2"),
  ("(fx- (fx- -1 2) (fx- 3 4))", L(S("fx-"), L(S("fx-"), -1, 2), L(S("fx-"), 3, 4)), "-2"),
  ("(fx- (fx- -1 2) (fx- 3 -4))", L(S("fx-"), L(S("fx-"), -1, 2), L(S("fx-"), 3, -4)), "-10"),
  ("(fx- (fx- -1 2) (fx- -3 4))", L(S("fx-"), L(S("fx-"), -1, 2), L(S("fx-"), -3, 4)), "4"),
  ("(fx- (fx- -1 2) (fx- -3 -4))", L(S("fx-"), L(S("fx-"), -1, 2), L(S("fx-"), -3, -4)), "-4"),
  ("(fx- (fx- -1 -2) (fx- 3 4))", L(S("fx-"), L(S("fx-"), -1, -2), L(S("fx-"), 3, 4)), "2"),
  ("(fx- (fx- -1 -2) (fx- 3 -4))", L(S("fx-"), L(S("fx-"), -1, -2), L(S("fx-"), 3, -4)), "-6"),
  ("(fx- (fx- -1 -2) (fx- -3 4))", L(S("fx-"), L(S("fx-"), -1, -2), L(S("fx-"), -3, 4)), "8"),
  ("(fx- (fx- -1 -2) (fx- -3 -4))", L(S("fx-"), L(S("fx-"), -1, -2), L(S("fx-"), -3, -4)), "0"),
  ("(fx- (fx- (fx- (fx- (fx- (fx- (fx- (fx- 1 2) 3) 4) 5) 6) 7) 8) 9)",
   L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), 1, 2), 3), 4), 5), 6), 7), 8), 9), "-43"),
  ("(fx- 1 (fx- 2 (fx- 3 (fx- 4 (fx- 5 (fx- 6 (fx- 7 (fx- 8 9))))))))",
   L(S("fx-"), 1, L(S("fx-"), 2, L(S("fx-"), 3, L(S("fx-"), 4, L(S("fx-"), 5, L(S("fx-"), 6, L(S("fx-"), 7, L(S("fx-"), 8, 9)))))))), "5"),
  ("(fx- (fx- (fx- (fx- 1 2) (fx- 3 4)) (fx- (fx- 5 6) (fx- 7 8))) (fx- (fx- (fx- 9 10) (fx- 11 12)) (fx- (fx- 13 14) (fx- 15 16))))",
   L(S("fx-"), L(S("fx-"), L(S("fx-"), L(S("fx-"), 1, 2), L(S("fx-"), 3, 4)), L(S("fx-"), L(S("fx-"), 5, 6), L(S("fx-"), 7, 8))), L(S("fx-"), L(S("fx-"), L(S("fx-"), 9, 10), L(S("fx-"), 11, 12)), L(S("fx-"), L(S("fx-"), 13, 14), L(S("fx-"), 15, 16)))), "0"),
  ("(fx* (fx* (fx* (fx* 2 3) (fx* 4 5)) (fx* (fx* 6 7) (fx* 8 9))) (fx* (fx* (fx* 2 3) (fx* 2 3)) (fx* (fx* 2 3) (fx* 2 3))))",
   L(S("fx*"), L(S("fx*"), L(S("fx*"), L(S("fx*"), 2, 3), L(S("fx*"), 4, 5)), L(S("fx*"), L(S("fx*"), 6, 7), L(S("fx*"), 8, 9))), L(S("fx*"), L(S("fx*"), L(S("fx*"), 2, 3), L(S("fx*"), 2, 3)), L(S("fx*"), L(S("fx*"), 2, 3), L(S("fx*"), 2, 3)))), "470292480"),
  ("(fxlognot (fxlogor (fxlognot 7) 1))", L(S("fxlognot"), L(S("fxlogor"), L(S("fxlognot"), 7), 1)), "6"),
  ("(fxlognot (fxlogor (fxlognot 7) (fxlognot 2)))", L(S("fxlognot"), L(S("fxlogor"), L(S("fxlognot"), 7), L(S("fxlognot"), 2))), "2"),
  ("(fxlogand (fxlognot (fxlognot 12)) (fxlognot (fxlognot 12)))", L(S("fxlogand"), L(S("fxlognot"), L(S("fxlognot"), 12)), L(S("fxlognot"), L(S("fxlognot"), 12))), "12"),
  ("(fx= (fx+ 13 3) (fx+ 10 6))", L(S("fx="), L(S("fx+"), 13, 3), L(S("fx+"), 10, 6)), "#t"),
  ("(fx= (fx+ 13 0) (fx+ 10 6))", L(S("fx="), L(S("fx+"), 13, 0), L(S("fx+"), 10, 6)), "#f"),
  ("(fx= (fx+ 12 1) (fx+ -12 -1))", L(S("fx="), L(S("fx+"), 12, 1), L(S("fx+"), -12, -1)), "#f"),
  ("(fx< (fx+ 10 6) (fx+ 13 1))", L(S("fx<"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 1)), "#f"),
  ("(fx< (fx+ 10 6) (fx+ 13 3))", L(S("fx<"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 3)), "#f"),
  ("(fx< (fx+ 10 6) (fx+ 13 31))", L(S("fx<"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 31)), "#t"),
  ("(fx< (fx+ 12 1) (fx+ -12 -1))", L(S("fx<"), L(S("fx+"), 12, 1), L(S("fx+"), -12, -1)), "#f"),
  ("(fx< (fx+ -12 -1) (fx+ 12 1))", L(S("fx<"), L(S("fx+"), -12, -1), L(S("fx+"), 12, 1)), "#t"),
  ("(fx<= (fx+ 10 6) (fx+ 13 1))", L(S("fx<="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 1)), "#f"),
  ("(fx<= (fx+ 10 6) (fx+ 13 3))", L(S("fx<="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 3)), "#t"),
  ("(fx<= (fx+ 10 6) (fx+ 13 31))", L(S("fx<="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 31)), "#t"),
  ("(fx<= (fx+ 12 1) (fx+ -12 -1))", L(S("fx<="), L(S("fx+"), 12, 1), L(S("fx+"), -12, -1)), "#f"),
  ("(fx<= (fx+ -12 -1) (fx+ 12 1))", L(S("fx<="), L(S("fx+"), -12, -1), L(S("fx+"), 12, 1)), "#t"),
  ("(fx> (fx+ 10 6) (fx+ 13 1))", L(S("fx>"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 1)), "#t"),
  ("(fx> (fx+ 10 6) (fx+ 13 3))", L(S("fx>"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 3)), "#f"),
  ("(fx> (fx+ 10 6) (fx+ 13 31))", L(S("fx>"), L(S("fx+"), 10, 6), L(S("fx+"), 13, 31)), "#f"),
  ("(fx> (fx+ 12 1) (fx+ -12 -1))", L(S("fx>"), L(S("fx+"), 12, 1), L(S("fx+"), -12, -1)), "#t"),
  ("(fx> (fx+ -12 -1) (fx+ 12 1))", L(S("fx>"), L(S("fx+"), -12, -1), L(S("fx+"), 12, 1)), "#f"),
  ("(fx>= (fx+ 10 6) (fx+ 13 1))", L(S("fx>="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 1)), "#t"),
  ("(fx>= (fx+ 10 6) (fx+ 13 3))", L(S("fx>="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 3)), "#t"),
  ("(fx>= (fx+ 10 6) (fx+ 13 31))", L(S("fx>="), L(S("fx+"), 10, 6), L(S("fx+"), 13, 31)), "#f"),
  ("(fx>= (fx+ 12 1) (fx+ -12 -1))", L(S("fx>="), L(S("fx+"), 12, 1), L(S("fx+"), -12, -1)), "#t"),
  ("(fx>= (fx+ -12 -1) (fx+ 12 1))", L(S("fx>="), L(S("fx+"), -12, -1), L(S("fx+"), 12, 1)), "#f"),
  )),

("let",
 (
  ("(let ([x 5]) x)", L(S("let"), L(L(S("x"), 5)), S("x")),"5"),
  ("(let ([x (fx+ 1 2)]) x)", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2))), S("x")),"3"),
  ("(let ([x (fx+ 1 2)]) (let ([y (fx+ 3 4)]) (fx+ x y)))", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2))), L(S("let"), L(L(S("y"), L(S("fx+"), 3, 4))), L(S("fx+"), S("x"), S("y")))),"10"),
  ("(let ([x (fx+ 1 2)]) (let ([y (fx+ 3 4)]) (fx- y x)))", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2))), L(S("let"), L(L(S("y"), L(S("fx+"), 3, 4))), L(S("fx-"), S("y"), S("x")))),"4"),
  ("(let ([x (fx+ 1 2)] [y (fx+ 3 4)]) (fx- y x))", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2)), L(S("y"), L(S("fx+"), 3, 4))), L(S("fx-"), S("y"), S("x"))),"4"),
  ("(let ([x (let ([y (fx+ 1 2)]) (fx* y y))]) (fx+ x x))", L(S("let"), L(L(S("x"), L(S("let"), L(L(S("y"), L(S("fx+"), 1, 2))), L(S("fx*"), S("y"), S("y"))))), L(S("fx+"), S("x"), S("x"))),"18"),
  ("(let ([x (fx+ 1 2)]) (let ([x (fx+ 3 4)]) x))", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2))), L(S("let"), L(L(S("x"), L(S("fx+"), 3, 4))), S("x"))),"7"),
  ("(let ([x (fx+ 1 2)]) (let ([x (fx+ x 4)]) x))", L(S("let"), L(L(S("x"), L(S("fx+"), 1, 2))), L(S("let"), L(L(S("x"), L(S("fx+"), S("x"), 4))), S("x"))),"7"),
  ("(let ([t (let ([t (let ([t (let ([t (fx+ 1 2)]) t)]) t)]) t)]) t)", L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("fx+"), 1, 2))), S("t")))), S("t")))), S("t")))), S("t")),"3"),
  ("(let ([x 12]) (let ([x (fx+ x x)]) (let ([x (fx+ x x)]) (let ([x (fx+ x x)]) (fx+ x x)))))", L(S("let"), L(L(S("x"), 12)), L(S("let"), L(L(S("x"), L(S("fx+"), S("x"), S("x")))), L(S("let"), L(L(S("x"), L(S("fx+"), S("x"), S("x")))), L(S("let"), L(L(S("x"), L(S("fx+"), S("x"), S("x")))), L(S("fx+"), S("x"), S("x")))))),"192"),
  )),

("cons",
 (("($fxadd1 0)", L(S("$fxadd1"), 0), "1"),
  ("(pair? (cons 1 2))", L(S("pair?"), L(S("cons"), 1, 2)), "#t"),
  ("(pair? 12)", L(S("pair?"), 12), "#f"),
  ("(pair? #t)", L(S("pair?"), True), "#f"),
  ("(pair? #f)", L(S("pair?"), False), "#f"),
  ("(pair? ())", L(S("pair?"), L()), "#f"),
  ("(fixnum? (cons 12 43))", L(S("fixnum?"), L(S("cons"), 12, 43)), "#f"),
  ("(boolean? (cons 12 43))", L(S("boolean?"), L(S("cons"), 12, 43)), "#f"),
  ("(null? (cons 12 43))", L(S("null?"), L(S("cons"), 12, 43)), "#f"),
  ("(not (cons 12 43))", L(S("not"), L(S("cons"), 12, 43)), "#f"),
  ("(if (cons 12 43) 32 43)", L(S("if"), L(S("cons"), 12, 43), 32, 43), "32"),
  ("(car (cons 1 23))", L(S("car"), L(S("cons"), 1, 23)), "1"),
  ("(cdr (cons 43 123))", L(S("cdr"), L(S("cons"), 43, 123)), "123"),
  ("(car (car (cons (cons 12 3) (cons #t #f))))", L(S("car"), L(S("car"), L(S("cons"), L(S("cons"), 12, 3), L(S("cons"), True, False)))), "12"),
  ("(cdr (car (cons (cons 12 3) (cons #t #f))))", L(S("cdr"), L(S("car"), L(S("cons"), L(S("cons"), 12, 3), L(S("cons"), True, False)))), "3"),
  ("(car (cdr (cons (cons 12 3) (cons #t #f))))", L(S("car"), L(S("cdr"), L(S("cons"), L(S("cons"), 12, 3), L(S("cons"), True, False)))), "#t"),
  ("(cdr (cdr (cons (cons 12 3) (cons #t #f))))", L(S("cdr"), L(S("cdr"), L(S("cons"), L(S("cons"), 12, 3), L(S("cons"), True, False)))), "#f"),
  ("(let ([x (let ([y (fx+ 1 2)]) (fx* y y))]) (cons x (fx+ x x)))", L(S("let"), L(L(S("x"), L(S("let"), L(L(S("y"), L(S("fx+"), 1, 2))), L(S("fx*"), S("y"), S("y"))))), L(S("cons"), S("x"), L(S("fx+"), S("x"), S("x")))), "(9 . 18)"),
  ("(let ([t0 (cons 1 2)] [t1 (cons 3 4)]) (let ([a0 (car t0)] [a1 (car t1)] [d0 (cdr t0)] [d1 (cdr t1)]) (let ([t0 (cons a0 d1)] [t1 (cons a1 d0)]) (cons t0 t1))))", L(S("let"), L(L(S("t0"), L(S("cons"), 1, 2)), L(S("t1"), L(S("cons"), 3, 4))), L(S("let"), L(L(S("a0"), L(S("car"), S("t0"))), L(S("a1"), L(S("car"), S("t1"))), L(S("d0"), L(S("cdr"), S("t0"))), L(S("d1"), L(S("cdr"), S("t1")))), L(S("let"), L(L(S("t0"), L(S("cons"), S("a0"), S("d1"))), L(S("t1"), L(S("cons"), S("a1"), S("d0")))), L(S("cons"), S("t0"), S("t1"))))), "((1 . 4) 3 . 2)"),
  ("(let ([t (cons 1 2)]) (let ([t t]) (let ([t t]) (let ([t t]) t))))", L(S("let"), L(L(S("t"), L(S("cons"), 1, 2))), L(S("let"), L(L(S("t"), S("t"))), L(S("let"), L(L(S("t"), S("t"))), L(S("let"), L(L(S("t"), S("t"))), S("t"))))), "(1 . 2)"),
  ("(let ([t (let ([t (let ([t (let ([t (cons 1 2)]) t)]) t)]) t)]) t)", L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("let"), L(L(S("t"), L(S("cons"), 1, 2))), S("t")))), S("t")))), S("t")))), S("t")), "(1 . 2)"),
  ("(cons 7 ())", None, "(7)"), # added by zjh
  ("(let ([x ()]) (let ([x (cons x x)]) x))", None, "(())"), # added by zjh
  ("(let ([x ()]) (let ([x (cons x x)]) (let ([x (cons x x)]) (let ([x (cons x x)]) (cons x x)))))", L(S("let"), L(L(S("x"), L())), L(S("let"), L(L(S("x"), L(S("cons"), S("x"), S("x")))), L(S("let"), L(L(S("x"), L(S("cons"), S("x"), S("x")))), L(S("let"), L(L(S("x"), L(S("cons"), S("x"), S("x")))), L(S("cons"), S("x"), S("x")))))), "((((()) ()) (()) ()) ((()) ()) (()) ())"),
  ("(cons (let ([x #t]) (let ([y (cons x x)]) (cons x y))) (cons (let ([x #f]) (let ([y (cons x x)]) (cons y x))) ()))", L(S("cons"), L(S("let"), L(L(S("x"), True)), L(S("let"), L(L(S("y"), L(S("cons"), S("x"), S("x")))), L(S("cons"), S("x"), S("y")))), L(S("cons"), L(S("let"), L(L(S("x"), False)), L(S("let"), L(L(S("y"), L(S("cons"), S("x"), S("x")))), L(S("cons"), S("y"), S("x")))), L())), "((#t #t . #t) ((#f . #f) . #f))"),
  )),

# added by zjh
("eq?",
 (("(eq? 3 3)", None, "#t"),
  ("(eq? 1 0)", None, "#f"),
  ("(let ([c (cons 1 2)]) (eq? c c))", None, "#t"),
  ("(let ([c1 (cons 1 2)] [c2 (cons 1 2)]) (eq? c1 c2))", None, "#f"),
  )),

("vectors",
 (("(vector? (make-vector 0))", None, "#t"),
  ("(vector-length (make-vector 12))", None, "12"),
  ("(vector? (cons 1 2))", None, "#f"),
  ("(vector? 1287)", None, "#f"),
  ("(vector? ())", None, "#f"),
  ("(vector? #t)", None, "#f"),
  ("(vector? #f)", None, "#f"),
  ("(pair? (make-vector 12))", None, "#f"),
  ("(null? (make-vector 12))", None, "#f"),
  ("(boolean? (make-vector 12))", None, "#f"),
  ("(make-vector 0)", None, "#()"),
  ("""(let ([v (make-vector 2)])
       (vector-set! v 0 #t)
       (vector-set! v 1 #f)
       v)""", None, "#(#t #f)"),
  ("""(let ([v (make-vector 2)])
       (vector-set! v 0 v)
       (vector-set! v 1 v)
       (eq? (vector-ref v 0) (vector-ref v 1)))""", None, "#t"),
  ("""(let ([v (make-vector 1)] [y (cons 1 2)])
       (vector-set! v 0 y)
       (cons y (eq? y (vector-ref v 0))))""", None, "((1 . 2) . #t)"),
  # added by zjh
  ("""(let ([v0 (make-vector 2)])
       (let ([v1 (make-vector 2)])
         (vector-set! v0 0 100)
         (vector-set! v0 1 200)
         (vector-set! v1 0 300)
         (vector-set! v1 1 400)
         v0))""", None, "#(100 200)"),
  ("""(let ([v0 (make-vector 2)])
       (let ([v1 (make-vector 2)])
         (vector-set! v0 0 100)
         (vector-set! v0 1 200)
         (vector-set! v1 0 300)
         (vector-set! v1 1 400)
         (cons v0 v1)))""", None, "(#(100 200) . #(300 400))"),

  ("""(let ([v0 (make-vector 3)])
       (let ([v1 (make-vector 3)])
         (vector-set! v0 0 100)
         (vector-set! v0 1 200)
         (vector-set! v0 2 150)
         (vector-set! v1 0 300)
         (vector-set! v1 1 400)
         (vector-set! v1 2 350)
         (cons v0 v1)))""", None, "(#(100 200 150) . #(300 400 350))"),
  ("""(let ([n 2])
    (let ([v0 (make-vector n)])
       (let ([v1 (make-vector n)])
         (vector-set! v0 0 100)
         (vector-set! v0 1 200)
         (vector-set! v1 0 300)
         (vector-set! v1 1 400)
         (cons v0 v1))))""", None, "(#(100 200) . #(300 400))"),
  ("""(let ([n 3])
    (let ([v0 (make-vector n)])
       (let ([v1 (make-vector (vector-length v0))])
         (vector-set! v0 (fx- (vector-length v0) 3) 100)
         (vector-set! v0 (fx- (vector-length v1) 2) 200)
         (vector-set! v0 (fx- (vector-length v0) 1) 150)
         (vector-set! v1 (fx- (vector-length v1) 3) 300)
         (vector-set! v1 (fx- (vector-length v0) 2) 400)
         (vector-set! v1 (fx- (vector-length v1) 1) 350)
         (cons v0 v1))))""", None, "(#(100 200 150) . #(300 400 350))"),
  ("""(let ([n 1])
       (vector-set! (make-vector n) ($fxsub1 n) (fx* n n))
       n)""", None, "1"),
  ("""(let ([n 1])
       (let ([v (make-vector 1)])
         (vector-set! v ($fxsub1 n) n)
         (vector-ref v ($fxsub1 n))))""", None, "1"),
  ("""(let ([v0 (make-vector 1)])
    (vector-set! v0 0 1)
    (let ([v1 (make-vector 1)])
        (vector-set! v1 0 13)
        (vector-set! (if (vector? v0) v0 v1)
             ($fxsub1 (vector-length (if (vector? v0) v0 v1)))
             ($fxadd1 (vector-ref
                        (if (vector? v0) v0 v1)
                        ($fxsub1 (vector-length (if (vector? v0) v0 v1))))))
        (cons v0 v1)))""", None, "(#(2) . #(13))"),
  )),


("strings",
 (("(string? (make-string 0))", None, "#t"),
  ("(make-string 0)", None, '""'),
  ("""(let ([s (make-string 1)])
       (string-set! s 0 #\\a)
       (string-ref s 0))""", None, "#\\a"),

  ("""(let ([s (make-string 2)])
       (string-set! s 0 #\\a)
       (string-set! s 1 #\\b)
       (cons (string-ref s 0) (string-ref s 1)))""", None, "(#\\a . #\\b)"),
  ("""(let ([i 0])
    (let ([s (make-string 1)])
       (string-set! s i #\\a)
       (string-ref s i)))""", None, "#\\a"),
  ("""(let ([i 0] [j 1])
    (let ([s (make-string 2)])
       (string-set! s i #\\a)
       (string-set! s j #\\b)
       (cons (string-ref s i) (string-ref s j))))""", None, "(#\\a . #\\b)"),
  ("""(let ([i 0] [c #\\a])
    (let ([s (make-string 1)])
       (string-set! s i c)
       (string-ref s i)))""", None, "#\\a"),
  ("(string-length (make-string 12))", None, "12"),
  ("(string? (make-vector 12))", None, "#f"),
  ("(string? (cons 1 2))", None, "#f"),
  ("(string? 1287)", None, "#f"),
  ("(string? ())", None, "#f"),
  ("(string? #t)", None, "#f"),
  ("(string? #f)", None, "#f"),
  ("(pair? (make-string 12))", None, "#f"),
  ("(null? (make-string 12))", None, "#f"),
  ("(boolean? (make-string 12))", None, "#f"),
  ("(vector? (make-string 12))", None, "#f"),
  ("(make-string 0)", None, '""'),
  ("""(let ([v (make-string 2)])
       (string-set! v 0 #\\t)
       (string-set! v 1 #\\f)
       v)""", None, "\"tf\""),
  ("""(let ([v (make-string 2)])
       (string-set! v 0 #\\x)
       (string-set! v 1 #\\x)
       (eq? (string-ref v 0) (string-ref v 1)))""", None, "#t"),
  ("""(let ([v0 (make-string 3)])
       (let ([v1 (make-string 3)])
         (string-set! v0 0 #\\a)
         (string-set! v0 1 #\\b)
         (string-set! v0 2 #\\c)
         (string-set! v1 0 #\\d)
         (string-set! v1 1 #\\e)
         (string-set! v1 2 #\\f)
         (cons v0 v1)))""", None, "(\"abc\" . \"def\")"),
  ("""(let ([n 2])
    (let ([v0 (make-string n)])
       (let ([v1 (make-string n)])
         (string-set! v0 0 #\\a)
         (string-set! v0 1 #\\b)
         (string-set! v1 0 #\\c)
         (string-set! v1 1 #\\d)
         (cons v0 v1))))""", None, "(\"ab\" . \"cd\")"),
  ("""(let ([n 3])
    (let ([v0 (make-string n)])
       (let ([v1 (make-string (string-length v0))])
         (string-set! v0 (fx- (string-length v0) 3) #\\a)
         (string-set! v0 (fx- (string-length v1) 2) #\\b)
         (string-set! v0 (fx- (string-length v0) 1) #\\c)
         (string-set! v1 (fx- (string-length v1) 3) #\\Z)
         (string-set! v1 (fx- (string-length v0) 2) #\\Y)
         (string-set! v1 (fx- (string-length v1) 1) #\\X)
         (cons v0 v1))))""", None,  "(\"abc\" . \"ZYX\")"),
  ("""(let ([n 1])
       (string-set! (make-string n) ($fxsub1 n) ($fixnum->char 34))
       n)""", None, "1"),
  ("""(let ([n 1])
       (let ([v (make-string 1)])
         (string-set! v ($fxsub1 n) ($fixnum->char n))
         ($char->fixnum (string-ref v ($fxsub1 n)))))""", None, "1"),
  ("""(let ([v0 (make-string 1)])
     (string-set! v0 0 #\\a)
     (let ([v1 (make-string 1)])
         (string-set! v1 0 #\\A)
         (string-set! (if (string? v0) v0 v1)
              ($fxsub1 (string-length (if (string? v0) v0 v1)))
              ($fixnum->char
                ($fxadd1
                   ($char->fixnum
                     (string-ref
                        (if (string? v0) v0 v1)
                        ($fxsub1 (string-length (if (string? v0) v0 v1))))))))
         (cons v0 v1)))""", None, "(\"b\" . \"A\")"),
  ("(let ([s (make-string 1)]) (string-set! s 0 #\\\") s)", None, '"\\""'),
  ("(let ([s (make-string 1)]) (string-set! s 0 #\\\\) s)", None, '"\\\\"'),
  )),

("procedures",
 (("(letrec () 12)", None, "12"),
  ("(letrec () (let ([x 5]) (fx+ x x)))", None, "10"),
  ("(letrec ([f (lambda () 5)]) 7)", None, "7"),
  ("(letrec ([f (lambda () 5)]) (let ([x 12]) x))", None, "12"),
  ("(letrec ([f (lambda () 5)]) (f))", None, "5"),
  ("(letrec ([f (lambda () 5)]) (let ([x (f)]) x))", None, "5"),
  ("(letrec ([f (lambda () 5)]) (fx+ (f) 6))", None, "11"),
  ("(letrec ([f (lambda () 5)]) (fx- 20 (f)))", None, "15"),
  ("(letrec ([f (lambda () 5)]) (fx+ (f) (f)))", None, "10"),
  ("""(letrec ([f (lambda () (fx+ 5 7))]
               [g (lambda () 13)])
              (fx+ (f) (g)))""", None, "25"),
  ("(letrec ([f (lambda (x) (fx+ x 12))]) (f 13))", None, "25"),
  ("(letrec ([f (lambda (x) (fx+ x 12))]) (f (f 10)))", None, "34"),
  ("(letrec ([f (lambda (x) (fx+ x 12))]) (f (f (f 0))))", None, "36"),
  ("""(letrec ([f (lambda (x y) (fx+ x y))]
               [g (lambda (x) (fx+ x 12))])
              (f 16 (f (g 0) (fx+ 1 (g 0)))))""", None, "41"),
  ("""(letrec ([f (lambda (x) (g x x))]
               [g (lambda (x y) (fx+ x y))])
              (f 12))""", None, "24"),
  ("""(letrec ([f (lambda (x)
                   (if (fxzero? x)
                       1
                       (fx* x (f ($fxsub1 x)))))])
        (f 5))""", None, "120"),
  ("""(letrec ([e (lambda (x) (if (fxzero? x) #t (o ($fxsub1 x))))]
               [o (lambda (x) (if (fxzero? x) #f (e ($fxsub1 x))))])
              (e 25))""", None, "#f"),
  )),


("deeply nested procedures",
 (("""(letrec ([sum (lambda (n ac)
                   (if (fxzero? n)
                        ac
                        (app sum ($fxsub1 n) (fx+ n ac))))])
    (app sum 10000 0))""", None, "50005000"),
  ("""(letrec ([e (lambda (x) (if (fxzero? x) #t (app o ($fxsub1 x))))]
            [o (lambda (x) (if (fxzero? x) #f (app e ($fxsub1 x))))])
     (app e 5000000))""", None, "#t"),
  )),


("begin/implicit-begin",
 (("(begin 12)", None, "12"),
  ("(begin 13 122)", None, "122"),
  ("(begin 123 2343 #t)", None, "#t"),
  ("(let ([t (begin 12 (cons 1 2))]) (begin t t))", None, "(1 . 2)"),
  ("(let ([t (begin 13 (cons 1 2))]) (cons 1 t) t)", None, "(1 . 2)"),
  ("(let ([t (cons 1 2)]) (if (pair? t) (begin t) 12))", None, "(1 . 2)"),
  )),

("set-car! set-cdr!",
 (("(let ([x (cons 1 2)]) (begin (set-cdr! x ()) x))", None, "(1)"),
  ("(let ([x (cons 1 2)]) (set-cdr! x ()) x)", None, "(1)"),
  ("(let ([x (cons 12 13)] [y (cons 14 15)]) (set-cdr! x y) x)", None, "(12 14 . 15)"),
  ("(let ([x (cons 12 13)] [y (cons 14 15)]) (set-cdr! y x) y)", None, "(14 12 . 13)"),
  ("(let ([x (cons 12 13)] [y (cons 14 15)]) (set-cdr! y x) x)", None, "(12 . 13)"),
  ("(let ([x (cons 12 13)] [y (cons 14 15)]) (set-cdr! x y) y)", None, "(14 . 15)"),
  ("(let ([x (let ([x (cons 1 2)]) (set-car! x #t) (set-cdr! x #f) x)]) (cons x x) x)", None, "(#t . #f)"),
  ("(let ([x (cons 1 2)]) (set-cdr! x x) (set-car! (cdr x) x) (cons (eq? x (car x)) (eq? x (cdr x))))", None, "(#t . #t)"),
  ("(let ([x #f]) (if (pair? x) (set-car! x 12) #f)q x)", None, "#f"),
# ;;;; ("(let ([x #f]) (if (pair? #f) (set-car! #f 12) #f) x)", None, "#f"),
  )),


# ;;; one possible implementation strategy for procedures is via closure
# ;;; conversion.
# ;;;
# ;;; Lambda does many things at the same time:
# ;;; 1) It creates a procedure object (ie. one that passes procedure?)
# ;;; 2) It contains both code (what to do when applied) and data (what
# ;;;    variables it references.
# ;;; 3) The procedure object, in addition to passing procedure?, can be
# ;;;    applied to arguments.
# ;;;
# ;;; First step: separate code from data:
# ;;; convert every program containing lambda to a program containing
# ;;; codes and closures:
# ;;; (let ([f (lambda () 12)]) (procedure? f))
# ;;; =>
# ;;; (codes ([f-code (code () () 12)])
# ;;;   (let ([f (closure f-code)])
# ;;;     (procedure? f)))
# ;;;
# ;;; The codes binds code names to code points.  Every code
# ;;; is of the form (code (formals ...) (free-vars ...) body)
# ;;;
# ;;; sexpr
# ;;;, None, recordize
# ;;; recognize lambda forms and applications
# ;;; =>
# ;;; (let ([y 12])
# ;;;   (let ([f (lambda (x) (fx+ y x))])
# ;;;     (fx+ (f 10) (f 0))))
# ;;;, None, convert closures
# ;;; (let ([y 12])
# ;;;   (let ([f (closure (code (x) (y) (fx+ x y)) y)])
# ;;;     (fx+ (call f 10) (call f 0))
# ;;;, None, lift codes
# ;;; (codes ([code0 (code (x) (y) (fx+ x y))])
# ;;;   (let ([y 12])
# ;;;     (let ([f (closure code0 y)])
# ;;;       (fx+ (call f 10) (call f 0)))))
# ;;;, None, code generation
# ;;; 1) codes form generates unique-labels for every code and
# ;;;    binds the names of the code to these labels.
# ;;; 2) Every code object has a list of formals and a list of free vars.
# ;;;    The formals are at stack locations -4(%esp), -8(%esp), -12(%esp), ...
# ;;;    The free vars are at -2(%edi), 2(%edi), 6(%edi), 10(%edi) ...
# ;;;    These are inserted in the environment and then the body of the code
# ;;;    is generated.
# ;;; 3) A (closure code-name free-vars ...) is generated the same way a
# ;;;    (vector val* ...) is generated:  First, the code-label and the free
# ;;;    variables are placed at 0(%ebp), 4(%ebp), 8(%ebp), etc..
# ;;;    A closure pointer is placed in %eax, and %ebp is incremented to the
# ;;;    next boundary.
# ;;; 4) A (call f arg* ...) does the following:
# ;;;    a) evaluates the args and places them at contiguous stack locations
# ;;;       si-8(%esp), si-12(%esp), ... (leaving room for two values).
# ;;;    b) The value of the current closure pointer, %edi, is saved on the
# ;;;       stack at si(%esp).
# ;;;    c) The closure pointer of the callee is loaded in %edi.
# ;;;    d) The value of %esp is adjusted by si
# ;;;    e) An indirect call to -6(%edi) is issued.
# ;;;    f) After return, the value of %esp is adjusted back by -si
# ;;;    g) The value of the closure pointer is restored.
# ;;;    The returned value is still in %eax.

("procedure?",
 (("(procedure? (lambda (x) x))", None, "#t"),
  ("(let ([f (lambda (x) x)]) (procedure? f))", None, "#t"),
  ("(procedure? (make-vector 0))", None, "#f"),
  ("(procedure? (make-string 0))", None, "#f"),
  ("(procedure? (cons 1 2))", None, "#f"),
  ("(procedure? #\S)", None, "#f"),
  ("(procedure? ())", None, "#f"),
  ("(procedure? #t)", None, "#f"),
  ("(procedure? #f)", None, "#f"),
  ("(string? (lambda (x) x))", None, "#f"),
  ("(vector? (lambda (x) x))", None, "#f"),
  ("(boolean? (lambda (x) x))", None, "#f"),
  ("(null? (lambda (x) x))", None, "#f"),
  ("(not (lambda (x) x))", None, "#f"),
  )),


("applying thunks",
 (("(let ([f (lambda () 12)]) (f))", None, "12"),
  ("(let ([f (lambda () (fx+ 12 13))]) (f))", None, "25"),
  ("(let ([f (lambda () 13)]) (fx+ (f) (f)))", None, "26"),
  ("""(let ([f (lambda ()
              (let ([g (lambda () (fx+ 2 3))])
                (fx* (g) (g))))])
    (fx+ (f) (f)))""", None, "50"),
  ("""(let ([f (lambda ()
              (let ([f (lambda () (fx+ 2 3))])
                (fx* (f) (f))))])
    (fx+ (f) (f)))""", None, "50"),
  ("""(let ([f (if (boolean? (lambda () 12))
                (lambda () 13)
                (lambda () 14))])
     (f))""", None, "14"),
  )),


("parameter passing",
 (("(let ([f (lambda (x) x)]) (f 12))", None, "12"),
  ("(let ([f (lambda (x y) (fx+ x y))]) (f 12 13))", None, "25"),
  ("""(let ([f (lambda (x)
              (let ([g (lambda (x y) (fx+ x y))])
                (g x 100)))])
    (f 1000))""", None, "1100"),
  ("""(let ([f (lambda (g) (g 2 13))])
     (f (lambda (n m) (fx* n m))))""", None, "26"),
  ("""(let ([f (lambda (g) (fx+ (g 10) (g 100)))])
    (f (lambda (x) (fx* x x))))""", None, "10100"),
  ("""(let ([f (lambda (f n m)
              (if (fxzero? n)
                  m
                  (f f ($fxsub1 n) (fx* n m))))])
    (f f 5 1))""", None, "120"),
  ("""(let ([f (lambda (f n)
              (if (fxzero? n)
                  1
                  (fx* n (f f ($fxsub1 n)))))])
    (f f 5))""", None, "120"),
  )),

("closures",
 (("""(let ([n 12])
     (let ([f (lambda () n)])
       (f)))""", None, "12"),
  ("""(let ([n 12])
     (let ([f (lambda (m) (fx+ n m))])
       (f 100)))""", None, "112"),
  ("""(let ([f (lambda (f n m)
              (if (fxzero? n)
                  m
                  (f ($fxsub1 n) (fx* n m))))])
    (let ([g (lambda (g n m) (f (lambda (n m) (g g n m)) n m))])
      (g g 5 1)))""", None, "120"),
  ("""(let ([f (lambda (f n)
              (if (fxzero? n)
                  1
                  (fx* n (f ($fxsub1 n)))))])
    (let ([g (lambda (g n) (f (lambda (n) (g g n)) n))])
      (g g 5)))""", None, "120"),
  )),

("set!",
 (("""(let ([x 12])
     (set! x 13)
     x)""", None, "13"),
  ("""(let ([x 12])
     (set! x ($fxadd1 x))
     x)""", None, "13"),
  ("""(let ([x 12])
     (let ([x #f]) (set! x 14))
     x)""", None, "12"),
  ("""(let ([x 12])
     (let ([y (let ([x #f]) (set! x 14))])
       x))""", None, "12"),
  ("""(let ([f #f])
     (let ([g (lambda () f)])
       (set! f 10)
       (g)))""", None, "10"),
  ("""(let ([f (lambda (x)
              (set! x ($fxadd1 x))
              x)])
     (f 12))""", None, "13"),
  ("""(let ([x 10])
     (let ([f (lambda (x)
                (set! x ($fxadd1 x))
                x)])
       (cons x (f x))))""", None, "(10 . 11)"),
  ("""(let ([t #f])
     (let ([locative
          (cons
             (lambda () t)
             (lambda (n) (set! t n)))])
       ((cdr locative) 17)
       ((car locative))))""", None, "17"),
  ("""(let ([locative
          (let ([t #f])
            (cons
              (lambda () t)
              (lambda (n) (set! t n))))])
      ((cdr locative) 17)
      ((car locative)))""", None, "17"),
  ("""(let ([make-counter
          (lambda ()
            (let ([counter -1])
              (lambda ()
                (set! counter ($fxadd1 counter))
                counter)))])
     (let ([c0 (make-counter)]
           [c1 (make-counter)])
       (c0)
       (cons (c0) (c1))))""", None, "(1 . 0)"),
  ("""(let ([fact #f])
     (set! fact (lambda (n)
                  (if (fxzero? n)
                      1
                      (fx* n (fact ($fxsub1 n))))))
     (fact 5))""", None, "120"),
  ("""(let ([fact #f])
     ((begin
         (set! fact (lambda (n)
                      (if (fxzero? n)
                          1
                          (fx* n (fact ($fxsub1 n))))))
         fact)
      5))""", None, "120"),
  )),

("complex constants",
 (("'42", None, "42"),
  ("'(1 . 2)", None, "(1 . 2)"),
  ("'(1 2 3)", None, "(1 2 3)"),
  ("(let ([x '(1 2 3)]) x)", None, "(1 2 3)"),
  ("(let ([f (lambda () '(1 2 3))]) (f))", None, "(1 2 3)"),
  ("(let ([f (lambda () '(1 2 3))]) (eq? (f) (f)))", None, "#t"),
  ("(let ([f (lambda () (lambda () '(1 2 3)))]) ((f)))", None, "(1 2 3)"),
  ("(let ([x '#(1 2 3)]) (cons x (vector-ref x 0)))", None, "(#(1 2 3) . 1)"),
  ('"Hello World"', None, '"Hello World"'),
  ("'(\"Hello\" \"World\")", None, '("Hello" "World")'),
  )),

("letrec",
 (("(letrec () 12)", None, "12"),
  ("(letrec ([f 12]) f)", None, "12"),
  ("(letrec ([f 12] [g 13]) (fx+ f g))", None, "25"),
  ("""(letrec ([fact
               (lambda (n)
                 (if (fxzero? n)
                     1
                     (fx* n (fact ($fxsub1 n)))))])
      (fact 5))""", None, "120"),
  ("(letrec ([f 12] [g (lambda () f)]) (g))", None, "12"),
  ("(letrec ([f 12] [g (lambda (n) (set! f n))]) (g 130) f)", None, "130"),
  ("(letrec ([f (lambda (g) (set! f g) (f))]) (f (lambda () 12)))", None, "12"),
  ("""(letrec ([f (cons (lambda () f)
                        (lambda (x) (set! f x)))])
      (let ([g (car f)])
        ((cdr f) 100)
        (g)))""", None, "100"),
  ("(letrec ([f (letrec ([g (lambda (x) (fx* x 2))]) (lambda (n) (g (fx* n 2))))]) (f 12))", None, "48"),
  ("""(letrec ([f (lambda (f n)
                    (if (fxzero? n)
                        1
                        (fx* n (f f ($fxsub1 n)))))])
        (f f 5))""", None, "120"),
  ("""(let ([f (lambda (f)
                (lambda (n)
                   (if (fxzero? n)
                       1
                       (fx* n (f ($fxsub1 n))))))])
       (letrec ([fix
                 (lambda (f)
                   (f (lambda (n) ((fix f) n))))])
        ((fix f) 5)))""", None, "120"),
  )),

("letrec*",
 (("(letrec* () 12)", None, "12"),
  ("(letrec* ([f 12]) f)", None, "12"),
  ("(letrec* ([f 12] [g 13]) (fx+ f g))", None, "25"),
  ("""(letrec* ([fact
               (lambda (n)
                 (if (fxzero? n)
                     1
                     (fx* n (fact ($fxsub1 n)))))])
      (fact 5))""", None, "120"),
  ("(letrec* ([f 12] [g (lambda () f)]) (g))", None, "12"),
  ("(letrec* ([f 12] [g (lambda (n) (set! f n))]) (g 130) f)", None, "130"),
  ("(letrec* ([f (lambda (g) (set! f g) (f))]) (f (lambda () 12)))", None, "12"),
  ("""(letrec* ([f (cons (lambda () f)
                        (lambda (x) (set! f x)))])
      (let ([g (car f)])
        ((cdr f) 100)
        (g)))""", None, "100"),
  ("(letrec* ([f (letrec* ([g (lambda (x) (fx* x 2))]) (lambda (n) (g (fx* n 2))))]) (f 12))", None, "48"),
  ("""(letrec* ([f (lambda (f n)
                     (if (fxzero? n)
                         1
                         (fx* n (f f ($fxsub1 n)))))])
        (f f 5))""", None, "120"),
  ("""(let ([f (lambda (f)
                (lambda (n)
                   (if (fxzero? n)
                       1
                       (fx* n (f ($fxsub1 n))))))])
       (letrec* ([fix
                  (lambda (f)
                    (f (lambda (n) ((fix f) n))))])
        ((fix f) 5)))""", None, "120"),
  ("(letrec* ([a 12] [b (fx+ a 5)] [c (fx+ b a)]) c)", None, "29"),
  )),


("and/or",
 (("(and)", None, "#t"),
  ("(and 5)", None, "5"),
  ("(and #f)", None, "#f"),
  ("(and 5 6)", None, "6"),
  ("(and #f ((lambda (x) (x x)) (lambda (x) (x x))))", None, "#f"),
  ("(or)", None, "#f"),
  ("(or #t)", None, "#t"),
  ("(or 5)", None, "5"),
  ("(or 1 2 3)", None, "1"),
  ("(or (cons 1 2) ((lambda (x) (x x)) (lambda (x) (x x))))", None, "(1 . 2)"),
  ("(let ([if 12]) (or if 17))", None, "12"),
  ("(let ([if 12]) (and if 17))", None, "17"),
  ("(let ([let 8]) (or let 18))", None, "8"),
  ("(let ([let 8]) (and let 18))", None, "18"),
  ("(let ([t 1]) (and (begin (set! t ($fxadd1 t)) t) t))", None, "2"),
  ("(let ([t 1]) (or (begin (set! t ($fxadd1 t)) t) t))", None, "2"),
  )),


("when/unless",
 (("""(let ([x (cons 1 2)])
       (when (pair? x)
         (set-car! x (fx+ (car x) (cdr x))))
       x)""", None, "(3 . 2)"),
  ("""(let ([x (cons 1 2)])
       (when (pair? x)
         (set-car! x (fx+ (car x) (cdr x)))
         (set-car! x (fx+ (car x) (cdr x))))
       x)""", None, "(5 . 2)"),
  ("""(let ([x (cons 1 2)])
       (unless (fixnum? x)
         (set-car! x (fx+ (car x) (cdr x))))
       x)""", None, "(3 . 2)"),
  ("""(let ([x (cons 1 2)])
       (unless (fixnum? x)
         (set-car! x (fx+ (car x) (cdr x)))
         (set-car! x (fx+ (car x) (cdr x))))
       x)""", None, "(5 . 2)"),
  ("(let ([let 12]) (when let let let let let))", None, "12"),
  ("(let ([let #f]) (unless let let let let let))", None, "#f"),
  )),


("cond",
 (("(cond [1 2] [else 3])", None, "2"),
  ("(cond [1] [else 13])", None, "1"),
  ("(cond [#f #t] [#t #f])", None, "#f"),
  ("(cond [else 17])", None, "17"),
  ("(cond [#f] [#f 12] [12 13])", None, "13"),
  ("(cond [(cons 1 2), None, (lambda (x) (cdr x))])", None, "2"),
  ("(let ([else #t]) (cond [else 1287]))", None, "1287"),
  ("(let ([else 17]) (cond [else]))", None, "17"),
  ("(let ([else 17]) (cond [else, None, (lambda (x) x)]))", None, "17"),
  ("(let ([else #f]) (cond [else ((lambda (x) (x x)) (lambda (x) (x x)))]) else)", None, "#f"),
  ("(let ([=> 12]) (cond [12, None, 14] [else 17]))", None, "14"),
  ("(let ([=> 12]) (cond [=>]))", None, "12"),
  ("(let ([=> 12]) (cond [=> =>]))", None, "12"),
  ("(let ([=> 12]) (cond [=>, None, =>]))", None, "12"),
  ("(let ([let 12]) (cond [let, None, (lambda (x) (fx+ let x))] [else 14]))", None, "24"),
  )),

# ; vararg tests

("vararg not using rest argument",
 (("(let ([f (lambda args 12)]) (f))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10 20))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10 20 30))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10 20 30 40))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10 20 30 40 50))", None, "12"),
  ("(let ([f (lambda args 12)]) (f 10 20 30 40 50 60 70 80 90))", None, "12"),
  ("(let ([f (lambda (a0 . args) 12)]) (f 10))", None, "12"),
  ("(let ([f (lambda (a0 . args) a0)]) (f 10))", None, "10"),
  ("(let ([f (lambda (a0 . args) 12)]) (f 10 20))", None, "12"),
  ("(let ([f (lambda (a0 . args) a0)]) (f 10 20))", None, "10"),
  ("(let ([f (lambda (a0 . args) 12)]) (f 10 20 30))", None, "12"),
  ("(let ([f (lambda (a0 . args) a0)]) (f 10 20 30))", None, "10"),
  ("(let ([f (lambda (a0 . args) 12)]) (f 10 20 30 40))", None, "12"),
  ("(let ([f (lambda (a0 . args) a0)]) (f 10 20 30 40))", None, "10"),
  ("(let ([f (lambda (a0 a1 . args) (vector a0 a1))]) (f 10 20 30 40 50 60 70 80 90 100))", None, "#(10 20)"),
  ("(let ([f (lambda (a0 a1 a2 . args) (vector a0 a1 a2))]) (f 10 20 30 40 50 60 70 80 90 100))", None, "#(10 20 30)"),
  ("(let ([f (lambda (a0 a1 a2 a3 . args) (vector a0 a1 a2 a3))]) (f 10 20 30 40 50 60 70 80 90 100))", None, "#(10 20 30 40)"),
  ("(let ([f (lambda (a0 a1 a2 a3 a4 . args) (vector a0 a1 a2 a3 a4))]) (f 10 20 30 40 50 60 70 80 90 100))", None, "#(10 20 30 40 50)"),
  ("(let ([f (lambda (a0 a1 a2 a3 a4 a5 . args) (vector a0 a1 a2 a3 a4 a5))]) (f 10 20 30 40 50 60 70 80 90 100))", None, "#(10 20 30 40 50 60)"),
  )),


("vararg using rest argument",
 (("(let ([f (lambda args args)]) (f))", None, "()"),
  ("(let ([f (lambda args args)]) (f 10))", None, "(10)"),
  ("(let ([f (lambda args args)]) (f 10 20))", None, "(10 20)"),
  ("(let ([f (lambda args args)]) (f 10 20 30))", None, "(10 20 30)"),
  ("(let ([f (lambda args args)]) (f 10 20 30 40))", None, "(10 20 30 40)"),
  ("(let ([f (lambda (a0 . args) (vector a0 args))]) (f 10))", None, "#(10 ())"),
  ("(let ([f (lambda (a0 . args) (vector a0 args))]) (f 10 20))", None, "#(10 (20))"),
  ("(let ([f (lambda (a0 . args) (vector a0 args))]) (f 10 20 30))", None, "#(10 (20 30))"),
  ("(let ([f (lambda (a0 . args) (vector a0 args))]) (f 10 20 30 40))", None, "#(10 (20 30 40))"),
  ("(let ([f (lambda (a0 a1 . args) (vector a0 a1 args))]) (f 10 20 30 40 50 60 70 80 90))", None, "#(10 20 (30 40 50 60 70 80 90))"),
  ("(let ([f (lambda (a0 a1 a2 . args) (vector a0 a1 a2 args))]) (f 10 20 30 40 50 60 70 80 90))", None, "#(10 20 30 (40 50 60 70 80 90))"),
  ("(let ([f (lambda (a0 a1 a2 a3 . args) (vector a0 a1 a2 a3 args))]) (f 10 20 30 40 50 60 70 80 90))", None, "#(10 20 30 40 (50 60 70 80 90))"),
  ("(let ([f (lambda (a0 a1 a2 a3 a4 . args) (vector a0 a1 a2 a3 a4 args))]) (f 10 20 30 40 50 60 70 80 90))", None, "#(10 20 30 40 50 (60 70 80 90))"),
  ("(let ([f (lambda (a0 a1 a2 a3 a4 a5 . args)(vector a0 a1 a2 a3 a4 a5 args))]) (f 10 20 30 40 50 60 70 80 90))", None, "#(10 20 30 40 50 60 (70 80 90))"),
  )),

("symbols",
 (("(symbol? 'foo)", None, "#t"),
  ("(symbol? '())", None, "#f"),
  ("(symbol? "")", None, "#f"),
  ("(symbol? '(1 2))", None, "#f"),
  ("(symbol? '#())", None, "#f"),
  ("(symbol? (lambda (x) x))", None, "#f"),
  ("(symbol? 'foo)", None, "#t"),
  ("(string? 'foo)", None, "#f"),
  ("(pair? 'foo)", None, "#f"),
  ("(vector? 'foo)", None, "#f"),
  ("(null? 'foo)", None, "#f"),
  ("(boolean? 'foo)", None, "#f"),
  ("(procedure? 'foo)", None, "#f"),
  ("(eq? 'foo 'bar)", None, "#f"),
  ("(eq? 'foo 'foo)", None, "#t"),
  ("'foo", None, "foo"),
  ("'(foo bar baz)", None, "(foo bar baz)"),
  ("'(foo foo foo foo foo foo foo foo foo foo foo)", None, "(foo foo foo foo foo foo foo foo foo foo foo)"),
  )),

("exit",
 (('(foreign-call "exit" 0)', None, ""),
  )),

("S_error",
 (("""(let ([error (lambda args
                   (foreign-call "ik_error" args))])
     (error #f "died")
     12)""", None, ""),

  ("""(let ([error (lambda args
                   (foreign-call "ik_error" args))])
     (error 'car "died")
     12)""", None, ""),
  )),


("vector",
 (("(fx= 1 2)", None, "#f"),
  ("(vector 1 2 3 4 5)", None, "#(1 2 3 4 5)"),
  ("(let ([f (lambda (f) (f 1 2 3 4 5 6))]) (f vector))", None, "#(1 2 3 4 5 6)"),
  )),

("error",
 (("(error 'foo \"here\")", None, ""),
  )),


("apply error",
 (("(let ([f 6]) (f f))", None, ""),
  ("(let ([f 6]) (f (f)))", None, ""),
  ("(1 2 3)", None, ""),
  ("(1 (3 4))", None, ""),
  ("(let ([f (lambda () (1 2 3))]) 12)", None, "12"),
  )),

("arg-check for fixed-arg procedures",
 (("(let ([f (lambda () 12)]) (f))", None, "12"),
  ("(let ([f (lambda () 12)]) (f 1))", None, ""),
  ("(let ([f (lambda () 12)]) (f 1 2))", None, ""),
  ("(let ([f (lambda (x) (fx+ x x))]) (f))", None, ""),
  ("(let ([f (lambda (x) (fx+ x x))]) (f 1))", None, "2"),
  ("(let ([f (lambda (x) (fx+ x x))]) (f 1 2))", None, ""),
  ("(let ([f (lambda (x y) (fx* x (fx+ y y)))]) (f))", None, ""),
  ("(let ([f (lambda (x y) (fx* x (fx+ y y)))]) (f 2))", None, ""),
  ("(let ([f (lambda (x y) (fx* x (fx+ y y)))]) (f 2 3))", None, "12"),
  ("(let ([f (lambda (x y) (fx* x (fx+ y y)))]) (f 2 3 4))", None, ""),
  )),

("arg-check for var-arg procedures",
 (("(let ([f (lambda x x)]) (f))", None, "()"),
  ("(let ([f (lambda x x)]) (f 'a))", None, "(a)"),
  ("(let ([f (lambda x x)]) (f 'a 'b))", None, "(a b)"),
  ("(let ([f (lambda x x)]) (f 'a 'b 'c))", None, "(a b c)"),
  ("(let ([f (lambda x x)]) (f 'a 'b 'c 'd))", None, "(a b c d)"),

  ("(let ([f (lambda (x . rest) (vector x rest))]) (f))", None, ""),
  ("(let ([f (lambda (x . rest) (vector x rest))]) (f 'a))", None, "#(a ())"),
  ("(let ([f (lambda (x . rest) (vector x rest))]) (f 'a 'b))", None, "#(a (b))"),
  ("(let ([f (lambda (x . rest) (vector x rest))]) (f 'a 'b 'c))", None, "#(a (b c))"),
  ("(let ([f (lambda (x . rest) (vector x rest))]) (f 'a 'b 'c 'd))", None, "#(a (b c d))"),

  ("(let ([f (lambda (x y . rest) (vector x y rest))]) (f))", None, ""),
  ("(let ([f (lambda (x y . rest) (vector x y rest))]) (f 'a))", None, ""),
  ("(let ([f (lambda (x y . rest) (vector x y rest))]) (f 'a 'b))", None, "#(a b ())"),
  ("(let ([f (lambda (x y . rest) (vector x y rest))]) (f 'a 'b 'c))", None, "#(a b (c))"),
  ("(let ([f (lambda (x y . rest) (vector x y rest))]) (f 'a 'b 'c 'd))", None, "#(a b (c d))"),
  )),


# ;;; (add-tests-with-string-output "arg-check for primitives"
# ;;;   [(cons 1 2 3)", None, ""),
# ;;;   [(cons 1)", None, ""),
# ;;;   [(vector-ref '#() 1 2 3 4)", None, ""),
# ;;;   [(vector-ref)", None, ""),
# ;;;   [(vector)", None, "#()"),
# ;;;   [(string), None, "\"\""]
# ;;; )

("string-set! errors",
 (
# first with a fixed index
  ("(let ((t 1)) (and (begin (set! t ($fxadd1 t)) t) t))", None, "2"),
  ("(let ((f (if (boolean? (lambda () 12)) (lambda () 13) (lambda () 14)))) (f))", None, "14"),

  ("(let ([f 12]) (let ([g (lambda () f)]) (g)))", None, "12"),
  ("(fx< 1 2)", None, "#t"),
  ("(let ([f (lambda (x y) (fx< x y))]) (f 10 10))", None, "#f"),
  ("(fx< 10 10)", None, "#f"),
  ("(fx< 10 2)", None, "#f"),
  ("(fx<= 1 2)", None, "#t"),
  ("(fx<= 10 10)", None, "#t"),
  ("(fx<= 10 2)", None, "#f"),
#   #;[(let ([f
#       (lambda (s i c)
#     (unless (string? s)
#       (error 'string-set!1 "not a string ~s" s))
#     (unless (fixnum? i)
#       (error 'string-set!2 "invalid index ~s" i))
#     (if (fx< i ($string-length s))
#         #f
#         (error 's1 ""))
#     (unless (fx>= i 0)
#       (error 'string-set!3 "index ~s is out of range for ~s" i s))
#     (unless (and (fx< i (string-length s))
#                  (fx>= i 0))
#       (error 'string-set!3 "index ~s is out of range for ~s" i s))
#     (unless (char? c)
#       (error 'string-set!4 "not a char ~s" c))
#     ($string-set! s i c) 12)])
#    (let ([x ($string #\a #\b #\c)]
#          [y #\a])
#      (f x 8 y)))", None, ""),

  ("(let ([x 12]) (string-set! x 0 #\a))", None, ""),
  ("(let ([x (string #\a #\b #\c)] [y 12]) (string-set! x 0 y))", None, ""),
  ("(let ([x (string #\a #\b #\c)] [y 12]) (string-set! x 8 y))", None, ""),
  ("(let ([x (string #\a #\b #\c)] [y #\a]) (string-set! x 8 y))", None, ""),
  ("(let ([x (string #\a #\b #\c)]) (string-set! x 8 #\a))", None, ""),
  ("(let ([x (string #\a #\b #\c)] [y #\a]) (string-set! x -1 y))", None, ""),

#  ; next the general case
#  ;;; 6 kinds of errors:
#  ;;;   string is either:
#  ;;;     lex-non-string, run-non-string, lex-string, valid
#  ;;;   index is either:
#  ;;;     lex-invalid, runtime-non-fixnum, runtime-above, runtime-below, valid
#  ;;;   char is either:
#  ;;;     lex-invalid, runtime-non-char, valid.
#  ;;;  that's 4x5x3 = 60 tests!
#  ;;;  If we skip over the lexical string check, (since I don't do it),
#  ;;;  we have: 2x5x3 = 30 tests.

  ("(let ([s (string #\a #\b #\c)] [i 1] [c #\X]) (string-set! s i c) s)", None, "\"aXc\""),
  ("(let ([s (string #\a #\b #\c)] [i 1]) (string-set! s i #\X) s)", None, "\"aXc\""),
  ("(let ([s (string #\a #\b #\c)] [i 1] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s (string #\a #\b #\c)] [i 1] [c #\X]) (string-set! s 1 c) s)", None, "\"aXc\""),
  ("(let ([s (string #\a #\b #\c)] [i 1]) (string-set! s 1 #\X) s)", None, "\"aXc\""),
  ("(let ([s (string #\a #\b #\c)] [i 1] [c 'X]) (string-set! s 1 c) s)", None, ""),

  ("(let ([s (string #\a #\b #\c)] [i 3] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i 3]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i 3] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s (string #\a #\b #\c)] [i -10] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i -11]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i -1] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s (string #\a #\b #\c)] [i 'foo] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i 'foo]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s (string #\a #\b #\c)] [i 'foo] [c 'X]) (string-set! s i c) s)", None, ""),



  ("(let ([s '(string #\a #\b #\c)] [i 1] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 1]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 1] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s '(string #\a #\b #\c)] [i 1] [c #\X]) (string-set! s 1 c) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 1]) (string-set! s 1 #\X) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 1] [c 'X]) (string-set! s 1 c) s)", None, ""),

  ("(let ([s '(string #\a #\b #\c)] [i 3] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 3]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 3] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s '(string #\a #\b #\c)] [i -10] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i -11]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i -1] [c 'X]) (string-set! s i c) s)", None, ""),

  ("(let ([s '(string #\a #\b #\c)] [i 'foo] [c #\X]) (string-set! s i c) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 'foo]) (string-set! s i #\X) s)", None, ""),
  ("(let ([s '(string #\a #\b #\c)] [i 'foo] [c 'X]) (string-set! s i c) s)", None, ""),
  )),

("string errors",
 (("(let ([f (lambda (a b c) (string a b c))]) (f #\\a #\\b #\\c))", None, "\"abc\""),
  ("(let ([f (lambda (a b c) (string a b c))]) (f #\\a 12 #\\c))", None, ""),
  ("(let ([f string]) (f #\\a #\\b #\\c))", None, "\"abc\""),
  ("(let ([f string]) (f #\\a #\\b 'x))", None,  ""),
  ("(string #\\a #\\b #\\c)", None, "\"abc\""),
  ("(string #\\a #\\b #t)", None, ""),
  )),

("nontail apply",
 (("(let ([f (lambda () 12)]) (fx+ (apply f '()) 1))", None, "13"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (fx+ (apply f 13 '()) 1))", None, "26"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (fx+ (apply f (cons 13 '())) 1))", None, "26"),
  ("(let ([f (lambda (x y z) (fx+ x (fx* y z)))]) (fx+ (apply f 12 '(7 2)) 1))", None, "27"),
  ("(cons (apply vector '(1 2 3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 '(2 3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 '(3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 '(4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 '(5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 '(6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 '(7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 7 '(8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 7 8 ()) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  )),

("tail apply",
 (("(let ([f (lambda () 12)]) (apply f '()))", None, "12"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (apply f 13 '()))", None, "25"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (apply f (cons 13 '())))", None, "25"),
  ("(let ([f (lambda (x y z) (fx+ x (fx* y z)))]) (apply f 12 '(7 2)))", None, "26"),
  ("(apply vector '(1 2 3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 '(2 3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 '(3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 '(4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 '(5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 '(6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 '(7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 7 '(8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 7 8 ())", None, "#(1 2 3 4 5 6 7 8)"),
  )),

("nontail apply",
 (("(let ([f (lambda () 12)]) (fx+ (apply f '()) 1))", None, "13"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (fx+ (apply f 13 '()) 1))", None, "26"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (fx+ (apply f (cons 13 '())) 1))", None, "26"),
  ("(let ([f (lambda (x y z) (fx+ x (fx* y z)))]) (fx+ (apply f 12 '(7 2)) 1))", None, "27"),
  ("(cons (apply vector '(1 2 3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 '(2 3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 '(3 4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 '(4 5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 '(5 6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 '(6 7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 '(7 8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 7 '(8)) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  ("(cons (apply vector 1 2 3 4 5 6 7 8 ()) '())", None, "(#(1 2 3 4 5 6 7 8))"),
  )),

("tail apply",
 (("(let ([f (lambda () 12)]) (apply f '()))", None, "12"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (apply f 13 '()))", None, "25"),
  ("(let ([f (lambda (x) (fx+ x 12))]) (apply f (cons 13 '())))", None, "25"),
  ("(let ([f (lambda (x y z) (fx+ x (fx* y z)))]) (apply f 12 '(7 2)))", None, "26"),
  ("(apply vector '(1 2 3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 '(2 3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 '(3 4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 '(4 5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 '(5 6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 '(6 7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 '(7 8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 7 '(8))", None, "#(1 2 3 4 5 6 7 8)"),
  ("(apply vector 1 2 3 4 5 6 7 8 ())", None, "#(1 2 3 4 5 6 7 8)"),
  )),

("remainder/modulo/quotient",
 (("(fxquotient 16 4)", None, "4"),
  ("(fxquotient 5 2)", None, "2"),
  ("(fxquotient -45 7)", None, "-6"),
  ("(fxquotient 10 -3)", None, "-3"),
  ("(fxquotient -17 -9)", None, "1"),

  ("(fxremainder 16 4)", None, "0"),
  ("(fxremainder 5 2)", None, "1"),
  ("(fxremainder -45 7)", None, "-3"),
  ("(fxremainder 10 -3)", None, "1"),
  ("(fxremainder -17 -9)", None, "-8"),

  ("(fxmodulo  16  4)", None, "0"),
  ("(fxmodulo   5  2)", None, "1"),
  ("(fxmodulo -45  7)", None, "4"),
  ("(fxmodulo  10 -3)", None, "-2"),
  ("(fxmodulo -17 -9)", None, "-8"),
  ("(let ([t  4]) (fxmodulo  16 t))", None, "0"),
  ("(let ([t  2]) (fxmodulo   5 t))", None, "1"),
  ("(let ([t  7]) (fxmodulo -45 t))", None, "4"),
  ("(let ([t -3]) (fxmodulo  10 t))", None, "-2"),
  ("(let ([t -9]) (fxmodulo -17 t))", None, "-8"),
  )),

("write-char",
 (("""(begin
       (write-char #\\a)
       (flush-output-port (current-output-port))
       (exit))""", None, "a"),
  ("""(begin
       (write-char #\\a)
       (close-output-port (current-output-port))
       (exit))""", None, "a"),
  ("""(begin
       (write-char #\\H)
       (write-char #\\e)
       (write-char #\\l)
       (write-char #\\l)
       (write-char #\\o)
       (write-char #\\space)
       (flush-output-port)
       (write-char #\\W)
       (write-char #\\o)
       (write-char #\\r)
       (write-char #\\l)
       (write-char #\\d)
       (write-char #\\!)
       (flush-output-port (current-output-port))
       (exit))""", None, "Hello World!"),
  )),


("write/display",
 (("(fx+ -536870911 -1)", None, "-536870912"),
  ("""(begin
        (write '(1 2 3))
        (exit))""", None, "(1 2 3)"),
  ("""(begin
        (write '"Hello World!")
        (exit))""", None, "\"Hello World!\""),
  )),

("eof-object",
 (("(eof-object? (eof-object))", None, "#t"),
  ("(null? (eof-object))", None, "#f"),
  ("(boolean? (eof-object))", None, "#f"),
  ("(string? (eof-object))", None, "#f"),
  ("(char? (eof-object))", None, "#f"),
  ("(pair? (eof-object))", None, "#f"),
  ("(symbol? (eof-object))", None, "#f"),
  ("(procedure? (eof-object))", None, "#f"),
  ("(vector? (eof-object))", None, "#f"),
  ("(not (eof-object))", None, "#f"),
  ("(eof-object? #\\a)", None, "#f"),
  ("(eof-object? #t)", None, "#f"),
  ("(eof-object? 12)", None, "#f"),
  ("(eof-object? '(1 2 3))", None, "#f"),
  ("(eof-object? '())", None, "#f"),
  ("(eof-object? '#(foo))", None, "#f"),
  ("(eof-object? (lambda (x) x))", None, "#f"),
  ("(eof-object? 'baz)", None, "#f"),
  )),

("read-char",
 (("""(begin
        (let ([p (open-output-file "stst.tmp" 'replace)])
          (display "Hello World!" p)
          (close-output-port p))
        (let ([p (open-input-file "stst.tmp")])
          (define loop
            (lambda ()
              (let ([x (read-char p)])
                (if (eof-object? x)
                    (begin
                      (close-input-port p)
                      '())
                    (begin
                      (display x)
                      (loop))))))
          (loop))
        (exit))""", None, "Hello World!"),
  ("""(let ([s (make-string 10000)]
            [t "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12344567890<>,./?;:'\"[]{}\\|`~!@#$%^&*()-_=+"])
        (define fill-string!
          (lambda (i j)
            (unless (fx= i (string-length s))
              (if (fx>= j (string-length t))
                  (fill-string! i (fx- j (string-length t)))
                  (begin
                    (string-set! s i (string-ref t j))
                    (fill-string! ($fxadd1 i) (fx+ j 17)))))))
        (define write-string!
          (lambda (i p)
            (cond
              [(fx= i (string-length s)) (close-output-port p)]
              [else
               (write-char (string-ref s i) p)
               (write-string! ($fxadd1 i) p)])))
        (define verify
          (lambda (i p)
            (let ([x (read-char p)])
              (cond
                [(eof-object? x)
                 (close-input-port p)
                 (fx= i (string-length s))]
                [(fx= i (string-length s)) (error 'verify "file too short")]
                [(eq? (string-ref s i) x)
                 (verify ($fxadd1 i) p)]
                [else (error 'verify "mismatch")]))))
        (fill-string! 0 0)
        (write-string! 0 (open-output-file "stst.tmp" 'replace))
        (verify 0 (open-input-file "stst.tmp")))""", None, "#t"),
  )),

("tokenizer",
 (("""(let ()
        (define test-tokenizer
          (lambda (p)
            ;(display (input-port? p) (standard-error-port))
            (let ([tok (read-token p)])
              (cond
               [(eof-object? tok) 'ok]
               [(or (eq? tok 'lparen)
                    (eq? tok 'rparen)
                    (eq? tok 'vparen)
                    (eq? tok 'lbrack)
                    (eq? tok 'rbrack)
                    (eq? tok 'dot)
                    (and (pair? tok)
                         (or (eq? (car tok) 'datum)
                             (eq? (car tok) 'macro))))
                (test-tokenizer p)]
               [else
                (display tok)
                (error 'test "Invalid token ~s" tok)]))))
        (define test-file
          (lambda (filename)
            (display "Testing " (standard-error-port))
            (display filename (standard-error-port))
            (display "..." (standard-error-port))
            (let ([p (open-input-file filename)])
            ;  (display (input-port? p)(standard-error-port))
              (test-tokenizer p))))
        (define test-files
          (lambda (files)
            (unless (null? files)
              (test-file (car files))
              (test-files (cdr files)))))
        (define filenames
          '("libsymboltable-3.3.ss"
            "libhandlers-3.3.ss"
            "libcore-4.3.ss"
            "libio-4.2.ss"
            "libwriter-4.1.ss"
            "libtokenizer-4.3.ss"
            "compiler-4.3.ss"))
        (when (null? filenames)
          (error 'no-files-provided-in-test "add them"))
        (test-files filenames)
        'ok)""", None, "ok"),
  )),


("reader",
 (("""(let ()
        (define test-reader
          (lambda (p)
            (let ([x (read p)])
              (cond
               [(eof-object? x) 'ok]
               [else (test-reader p)]))))
        (define test-file
          (lambda (filename)
            (display "Testing " (standard-error-port))
            (display filename (standard-error-port))
            (display "..." (standard-error-port))
            (test-reader (open-input-file filename))))
        (define test-files
          (lambda (files)
            (unless (null? files)
              (test-file (car files))
              (test-files (cdr files)))))
        (define filenames
          '("libsymboltable-3.3.ss"
            "libhandlers-3.3.ss"
            "libcore-4.3.ss"
            "libio-4.2.ss"
            "libwriter-4.1.ss"
            "libtokenizer-4.3.ss"
            "compiler-4.3.ss"))
        (when (null? filenames)
          (error 'no-files-provided-in-test "add them"))
        (test-files filenames)
        'ok)""", None, "ok"),
  )),

("tokenizer",
 (("""(let ()
        (define test-tokenizer
          (lambda (p)
            ;(display (input-port? p) (standard-error-port))
            (let ([tok (read-token p)])
              (cond
               [(eof-object? tok) 'ok]
               [(or (eq? tok 'lparen)
                    (eq? tok 'rparen)
                    (eq? tok 'vparen)
                    (eq? tok 'lbrack)
                    (eq? tok 'rbrack)
                    (eq? tok 'dot)
                    (and (pair? tok)
                         (or (eq? (car tok) 'datum)
                             (eq? (car tok) 'macro))))
                (test-tokenizer p)]
               [else
                (display tok)
                (error 'test "Invalid token ~s" tok)]))))
        (define test-file
          (lambda (filename)
            (display "Testing " (standard-error-port))
            (display filename (standard-error-port))
            (display "..." (standard-error-port))
            (let ([p (open-input-file filename)])
            ;  (display (input-port? p)(standard-error-port))
              (test-tokenizer p))))
        (define test-files
          (lambda (files)
            (unless (null? files)
              (test-file (car files))
              (test-files (cdr files)))))
        (define filenames
          '("libsymboltable-4.4.ss"
            "libhandlers-3.3.ss"
            "libcore-4.4.ss"
            "libio-4.2.ss"
            "libwriter-4.4.ss"
            "libtokenizer-4.3.ss"
            "compiler-5.1.ss"))
        (when (null? filenames)
          (error 'no-files-provided-in-test "add them"))
        (test-files filenames)
        'ok)""", None, "ok"),
  )),

("reader",
 (("""(let ()
        (define test-reader
          (lambda (p)
            (let ([x (read p)])
              (cond
               [(eof-object? x) 'ok]
               [else (test-reader p)]))))
        (define test-file
          (lambda (filename)
            (display "Testing " (standard-error-port))
            (display filename (standard-error-port))
            (display "..." (standard-error-port))
            (test-reader (open-input-file filename))))
        (define test-files
          (lambda (files)
            (unless (null? files)
              (test-file (car files))
              (test-files (cdr files)))))
        (define filenames
          '("libsymboltable-4.4.ss"
            "libhandlers-3.3.ss"
            "libcore-4.4.ss"
            "libio-4.2.ss"
            "libwriter-4.4.ss"
            "libtokenizer-4.3.ss"
            "compiler-5.1.ss"))
        (when (null? filenames)
          (error 'no-files-provided-in-test "add them"))
        (test-files filenames)
        'ok)""", None, "ok"),
  )),

("overflow",
 (("""(letrec ([f
        (lambda (i)
          (when (fx<= i 1000)
            (let ([x (make-list 1000)])
              (f ($fxadd1 i)))))])
       (f 0)
       100)""", None, "100"),
  ("""(letrec ([f
        (lambda (i)
          (when (fx<= i 100000)
            (let ([x (list 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                           0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0)])
              (f ($fxadd1 i)))))])
       (f 0)
       100)""", None, "100"),
  )),


("call/cc",
 (("(call/cc (lambda (k) 12))", None, "12"),
  ("(call/cc (lambda (k) (k 12)))", None, "12"),
  ("(call/cc (lambda (k) (fx+ 1 (k 12))))", None, "12"),
  ("(fx+ (call/cc (lambda (k) (k 12))) (call/cc (lambda (k) 13)))", None, "25"),
  ("""(letrec ([fact
                (lambda (n k)
                  (cond
                    [(fxzero? n) (k 1)]
                    [else (fx* n (fact ($fxsub1 n) k))]))])
        (call/cc
          (lambda (k)
            (fact 5 k))))""", None, "1"),
  ("""(call/cc
       (lambda (k)
         (letrec ([fact
                   (lambda (n)
                     (cond
                       [(fxzero? n) (k 1)]
                       [else (fx* n (fact ($fxsub1 n)))]))])
           (fact 5))))""", None, "1"),
  ("""(let ([k #f])
        (letrec ([fact
                  (lambda (n)
                    (cond
                      [(fxzero? n)
                       (call/cc
                         (lambda (nk)
                           (set! k nk)
                           (k 1)))]
                      [else (fx* n (fact ($fxsub1 n)))]))])
           (let ([v (fact 5)])
             v)))""", None, "120"),
  ("""(let ([k #f])
        (letrec ([fact
                  (lambda (n)
                    (cond
                      [(fxzero? n)
                       (call/cc
                         (lambda (nk)
                           (set! k nk)
                           (k 1)))]
                      [else (fx* n (fact ($fxsub1 n)))]))])
           (let ([v (fact 5)])
             (let ([nk k])
               (set! k (lambda (x) (cons v x)))
               (nk v)))))""", None, "(120 . 14400)"),
  )),
]

from parser import parse

start = 0
compile=True
if len(sys.argv)>1:
    start = int(sys.argv[1])
    if len(sys.argv)>2:
        assert sys.argv[2]=='nocompile'
        compile = False

start_time = time.time()
# Test parsing and (optionally, compilation)
for cat_count, (category, tests) in enumerate(TESTS[start:]):
    print("%d: %s" % (cat_count+start, category))
    for text, parse_e, result_e in tests:
        parse_a = parse(text)
        if parse_e is not None:
            assert parse_a == parse_e, "[%s]: %s != %s" % (text, parse_a, parse_e)
        if compile:
            result_a = compile_and_run(parse_a, text)
            assert result_a == result_e, "[%s]: %s != %s" % (text, result_a, result_e)
end_time = time.time()
print("--- time: %.2f seconds ---" % (end_time-start_time))
