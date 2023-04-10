import re
import unicodedata
from spellchecker import SpellChecker
from collections import Counter
from nltk.stem import PorterStemmer


def is_pua(c):
    return unicodedata.category(c) == "Co"


def remove_punct_nums(text):
    text = re.sub("[^a-z. ]", "", text)
    return text


def clean3(test: str):

    """
    input: string containing special characters, unicodes etc 
    output: clean string but containing numbers,commas, periods still
    
    """

    replacements = {
        "t-co2e": "tonnes co2 emissions",
        "tco2e": "tonnes co2 emissions",
        "co2e": "co2 emissions",
        "ghg": "greenhouse gas",
        "t-co2": "tonnes co2",
        "tco2": "tonnes co2",
        "t-c02": "tonnes co2",
        "tc02": "tonnes c02",
        "c02": "carbon dioxide",
        "co2": "carbon dioxide",
        "&": "and",
        "%": "",  # cent showing up too much
        "°c": " degrees celcius",
        "_x000c_": "",
        "appendix": "",
        "introduction": "",
        "contents": "",
        "glossary": "",
        "copyright": "",
        "author": "",
        "email": "",
        "sdgs": "sustainable development goals",
        "sdg": "sustainable development goal",
        "kwh": "kilowatt hour",
        "kg": "kilogram",
    }

    re_patterns = {
        "emails": "\S*@\S*\s?",
        "websites": "http\S+",
        "www-websites": "www\S+",
        ".pdfs": "\S+.pdf\b",
        ".com": "\S+.com\b",
        ".co.uk": "\S+.co.uk\b",
        "double-quotes": r'"([^"]+)"',
        "single-quotes": r"'([^']+)'",
        "abnormal long": "\b\w{21,}\b",
    }

    test = "".join([char for char in test if not is_pua(char)])
    test = " ".join(test.split())
    test = test.lower()

    for key in re_patterns:
        test = re.sub(re_patterns[key], "", test)

    for key in replacements:
        test = test.replace(key, replacements[key])

    #general rule based cleaning
    test = " ".join(test.split())
    test = re.sub("[#*;•♦£$\[\]]", ".", test)
    test = re.sub("[-/]", " ", test)
    test = re.sub("\.\s", ".", test)  
    test = re.sub("\.\.+", ".", test)
    test = re.sub("\([^)]+\)", "", test)
    test = re.sub("\s\d+(\s\d+)*\s", " ", test)
    test = re.sub("[:\-–_‘’]", " ", test)
    test = re.sub(r'"([^"]+)"', "\1", test)  # double quotes
    test = re.sub(r"'([^']+)'", "\1", test)  # single quotes
    test = re.sub(
        "((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(m|bn|,|\.|\s|\b)", "", test
    )  # getting rid of numbers
    #necessary to remove double full stops
    test = " ".join(test.split())
    test = re.sub("\.\.+", ".", test)
    test = " ".join(test.split())
    test = re.sub("[^a-z0-9., ]", "", test)
    test = " ".join(test.split())
    return test


def has_repeated_word(s):
    words = s.split()
    # Count the occurrences of each word
    word_counts = Counter(words)

    # Check if any word occurs more than once
    for count in word_counts.values():
        if count > 1:
            return True

    return False


def contains_digits(s):
    pattern = r"\d"
    if re.search(pattern, s):
        return True
    else:
        return False


def contains_misspelled_word(string):
    spell = SpellChecker(language="en")
    words = string.split()
    misspelled_words = spell.unknown(words)
    if len(misspelled_words) > 0:
        return True
    else:
        return False


def word_a_b_common_word(row):
    ps = PorterStemmer()
    words1 = set([ps.stem(word) for word in row["word_a"].split()])
    words2 = set([ps.stem(word) for word in row["word_b"].split()])
    return len(words1 & words2) > 0
