import warnings
def warn(*args, **kwargs):
    pass
warnings.warn = warn
from textblob import TextBlob

text = TextBlob("youre the best")
print(text.sentiment.polarity) 

