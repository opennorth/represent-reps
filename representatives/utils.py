from __future__ import unicode_literals


def boundary_url_to_name(s):
    s = s.replace('/boundaries/', '')
    if s.endswith('/'):
        return s[:-1]
    return s
