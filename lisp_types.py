class Char:
    SPECIALS = {
        " ": "space",
        "\n": "newline"
    }

    def __init__(self, ch):
        self.ch = ch

    def __str__(self):
        return self.ch

    def __repr__(self):
        return u"Char(%r)" % self.ch

    def display(self):
        return u"#\\%s" % self.SPECIALS.get(self.ch, self.ch)

class Symbol:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def display(self):
        return self.name

    def __repr__(self):
        return u"Symbol(%r)" % self.name
