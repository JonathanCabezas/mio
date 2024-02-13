accents_and_substitute = [
    ("éèêë", "e"),
    ("àâä", "a"),
    ("îï", "i"),
    ("ôö", "o"),
    ("ûü", "u"),
]
accents = ""
substitutes = ""
for a, s in accents_and_substitute:
    accents += a
    substitutes += s * len(a)
translation_table = str.maketrans(accents, substitutes)


def unaccentuate(msg):
    return msg.translate(translation_table)
