# Original Copyrights: Ruben Decrop
# modifications done by Chessdevil consulting BVBA

from django.conf import settings


translation_strings = {}

def translate(s, locale):
    """
    translate a string in a locale
    :param s: the string
    :param locale: the locale
    :return: the tranlated string or None if no translation is found
    """
    if locale not in translation_strings:
        log.warning('translation language %s not availbe (did you load it?)',
                    locale)
        return None
    value = translation_strings[locale].get(s)
    if not value:
        log.warning('no %s translation for %s', lang, s)
    return value


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
