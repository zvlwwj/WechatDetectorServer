import re
# Backport Python 3.4's regular expression "fullmatch()" to Python 2
def fullmatch(regex, string, flags=0):
    """Emulate python-3.4 re.fullmatch()."""
    return re.match("(?:" + regex + r")\Z", string, flags=flags)