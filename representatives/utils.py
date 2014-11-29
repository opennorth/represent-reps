from __future__ import unicode_literals

import re
import unicodedata

from django.utils.six import text_type


def get_comparison_string(s):
    """Given a string or unicode, returns a simplified lowercase whitespace-free ASCII string.
    Used to compare slightly different versions of the same thing, which may differ in case,
    spacing, or use of accents."""
    s = re.sub(r'[^a-zA-Z0-9]', '-', remove_accents(s.lower()))
    return re.sub(r'--+', '-', s)


def remove_accents(s):
    nkfd_form = unicodedata.normalize('NFKD', text_type(s))
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)])


def boundary_url_to_name(s):
    s = s.replace('/boundaries/', '')
    if s.endswith('/'):
        return s[:-1]
    return s


def split_name(n):
    """Given a name, returns (first_name, last_name)."""
    # Very simple implementation currently just splits out the last component.
    n_bits = n.split(' ')
    last = n_bits.pop()
    return ' '.join(n_bits), last
