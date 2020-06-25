import bs4 as bs
import urllib.request
import re
import nltk
import heapq
import sys

def help_menu():
    print('''USAGE:
python __init__.py [FILE_PATH] [SUMMARY_LENGTH]''')

fileAsArg = sys.argv[1] if len(sys.argv) > 1 else '' 
summaryLength = int(sys.argv[2]) if len(sys.argv) > 2 else 1

content = ""
_paragraphs = []
article_text = ""

if (fileAsArg and not ('http' in fileAsArg)):
    f = open(fileAsArg, 'r+')

    for line in f:
        _paragraphs.append(line)

    for p in _paragraphs:
        #article_text += p.text
        article_text += p

elif ('http' in fileAsArg):

    scraped_data = urllib.request.urlopen(fileAsArg)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    for p in paragraphs:
        article_text += p.text

else:

    help_menu()
    exit(0)

if __name__ == "__main__":

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}

    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_freq = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_freq)

    sentence_scores = {}

    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(summaryLength, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)

    print(summary)
