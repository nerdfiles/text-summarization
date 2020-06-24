import bs4 as bs
import urllib.request
import re
import nltk
import heapq


# scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
# article = scraped_data.read()
#
# parsed_article = bs.BeautifulSoup(article,'lxml')
#
# paragraphs = parsed_article.find_all('p')

#f = open('../four-word-phrase/example/discourse-on-method.txt', 'r+')
#f = open('../four-word-phrase/example/ethica.txt', 'r+')
#f = open('./prolegomenas-laruelle.txt', 'r+')
#f = open('./phil-decision.txt', 'r+')
f = open('./tlp.txt', 'r+')

content = ""
_paragraphs = []

for line in f:
    _paragraphs.append(line)

#print(_paragraphs)
article_text = ""

for p in _paragraphs:
    #article_text += p.text
    article_text += p

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

    #print(word_frequencies)
    maximum_freq = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_freq)

    #print(len(sentence_list))
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                #print(sent.split(' '))
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    #summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    #summary_sentences = heapq.nlargest(14, sentence_scores, key=sentence_scores.get)
    summary_sentences = heapq.nlargest(1, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)

    print(summary)
