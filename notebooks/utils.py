import re
import unicodedata
import spacy

import re
import unicodedata

def is_pua(c):
    return unicodedata.category(c) == 'Co'

replacements = {'co2e': 'co2 emissions',
              'ghg': 'greenhouse gas',
              'tco2': 'tonnes co2',
              'tc02': 'tonnes c02',
              'c02': 'carbon dioxide',
              'co2': 'carbon dioxide',
              'qtr': 'quarter',
              '&': 'and',
              '%': ' per cent',
              '°c': ' degrees celcius',
                '_x000c_': ''
         }

re_patterns = {'emails': "\S*@\S*\s?",
               'websites': "http\S+",
#                '2+ spaces': "\s\s+",
#                '2+ periods': "\.\.+",
               'brackets': "\([^)]+\)"
    
}

def clean2(text):
    
    text = ' '.join(text.split())
    text = text.lower()
    # regex replaced with nothing
    for key in re_patterns:
        text = re.sub(re_patterns[key], "", text)

    #replace abbreviations
    for key in replacements:
        text = text.replace(key, replacements[key])
        
    #remove unicode defects    
    text = "".join([char for char in text if not is_pua(char)]) 
    
    #regex replaced with space
    text = re.sub("-", " ",text)
    text = re.sub("/", " ",text)
    text = re.sub(":", ' ',text)
    text = re.sub("\s\s+", " ", text)

    text = re.sub("\.\.+", ".", text)
    
    
    #remove anything non-alphanumeric at end lower
    text = re.sub("[^a-z0-9., ]",'',text) 
    
    return text


def remove_punct_nums(text):
    text = re.sub("[^a-z.]",'',text)
    return text




# nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

# def lemmatize(text):
#     doc = nlp(text)
#     # Turn it into tokens, ignoring the punctuation
#     tokens = [token for token in doc if not token.is_punct]
#     # Convert those tokens into lemmas, EXCEPT the pronouns, we'll keep those.
#     lemmas = [token.lemma_ if token.pos_ != 'PRON' else token.orth_ for token in tokens]
#     return lemmas






if __name__ == '__main__':
    print('have fun my functions file')
    