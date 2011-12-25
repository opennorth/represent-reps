import re
import unicodedata

def slugify(s):
    s = re.sub(r'[^a-zA-Z]', '-', remove_accents(s))
    return re.sub(r'--+', '-', s)

def remove_accents(s):
    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])