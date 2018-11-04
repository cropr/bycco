# Original Copyrights: Ruben Decrop
# modifications done by Chessdevil consulting BVBA

from django.conf import settings

def to_int(s, default):
    """
    converts a strin to int with a default
    :param s: the str
    :param default: the default
    :return: the converted int
    """
    try:
         return int(s)
    except ValueError:
        return default
