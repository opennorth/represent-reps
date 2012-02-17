import re
import unicodedata

def get_comparison_string(s):
    """Given a string or unicode, returns a simplified lowercase whitespace-free ASCII string.
    Used to compare slightly different versions of the same thing, which may differ in case,
    spacing, or use of accents."""
    s = re.sub(r'[^a-zA-Z0-9]', '-', remove_accents(s.lower()))
    return re.sub(r'--+', '-', s)

def remove_accents(s):
    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def boundary_url_to_name(s):
    s = s.replace('/boundaries/', '')
    if s.endswith('/'):
        return s[:-1]
    return s

_r_honorific = re.compile(r'^(Hon|Mr|Mrs|Ms)\.?\s')
def strip_honorific(s):
    return _r_honorific.sub('', s)

def split_name(n):
    """Given a name, returns (first_name, last_name)."""
    # Very simple implementation currently just splits out the last component.
    n_bits = n.split(' ')
    last = n_bits.pop()
    return ' '.join(n_bits), last