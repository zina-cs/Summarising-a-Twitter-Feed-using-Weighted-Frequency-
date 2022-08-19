import re
import requests
import heapq
import nltk
from langcodes import Language
import eel
From Tweet.py import Tweet 


def summarise(stopwords, messages):
    freq = {}
    messages = re.sub(r'\[[0-9]*\]', ' ', messages)
    messages = re.sub(r'\s+', ' ', messages)
    messages = messages.replace("\\n", "")
    editedM = nltk.re.sub(r'\s+', ' ', messages)
    sentence_list = nltk.sent_tokenize(messages)
    tokenizedText = nltk.word_tokenize(editedM)
    for w in tokenizedText:
        if w not in stopwords:
            if w not in freq.keys():
                freq[w] = 1
            else:
                freq[w] += 1

    maxFreq = max(freq.values())

    for w in freq.keys():
        freq[w] = (freq[w] / maxFreq)

    sentenceVal = {}
    for s in sentence_list:
        for w in nltk.word_tokenize(s.lower()):
            if w in freq.keys():
                if len(s.split(' ')) < 30:
                    if s not in sentenceVal.keys():
                        sentenceVal[s] = freq[w]
                    else:
                        sentenceVal[s] += freq[w]
    print(sentenceVal)
    sentences = heapq.nlargest(7, sentenceVal, key=sentenceVal.get)
    output = ""
    for i in sentences:
        print(i)
        output += i
    return output



eel.init('web')


@eel.expose
def action():
    bearer_token = '<insert your bearer token here>'
    params = {"tweet.fields": "lang", "max_results": 100}
    website = "https://twitter.com/<Twitter-Account-Username"
    results = ""
    if website.count('/') == 3:
        urlCount = 0
        username = ""
        for i in website:
            urlCount += 1
            if urlCount > 20:
                username += i
        idurl = "https://api.twitter.com/2/users/by/username/" + username
        headers = {
            'Authorization': '<insert token for authorization here', }
        r = requests.get(idurl, headers=headers)
        idcount = 0
        id = ""
        for i in r.text:
            idcount += 1
            if (idcount > 15):
                if i == '"':
                    break
                else:
                    id += i
        print(id)
        url = "https://api.twitter.com/2/users/{}/tweets".format(id)
        request = requests.get(url, headers=headers, params=params)
        data = request.text[8:]
        print(data)
        tweet = list(data.split("]"))
        tweet = list(tweet[0].split("}"))
        tweets = []
        tweetCount = 0
        for i in tweet:
            tweetCount += 1
            tweets.append(i.split('"'))
            print(i.split('"'))
        Tweets = []
        lang = []
        langCount = 0
        for i in tweets:
            T = Tweet()
            if len(i) > 11:
                T.id = i[3]
                T.lang = i[7]
                T.message = i[11]
                x = T.message
                Tweets.append(T)
                if T.lang not in lang:
                    lang.append(T.lang)
                    langCount += 1

        for i in lang:
            if i == 'und':
                lang.remove('und')
                langCount -= 1
            print(i)
        l1 = Language.get(lang[0]).display_name()

        if langCount == 1:
            messages = ""
            for j in Tweets:
                messages += j.message
            stopwords = nltk.corpus.stopwords.words(l1)
            results = summarise(stopwords, messages)
        elif langCount > 1:
            lang1 = ""
            lang2 = ""
            for j in Tweets:
                if j.lang == lang[0]:
                    lang1 += j.message
                if j.lang == lang[1]:
                    lang2 += j.message
            l2 = Language.get(lang[1]).display_name()
            stopwords = nltk.corpus.stopwords.words(l1)
            results = summarise(stopwords, lang1)
            try:
                stopwords = nltk.corpus.stopwords.words(l2)
            except OSError:
                stopwords = nltk.corpus.stopwords.words("english")
            results += summarise(stopwords, lang2)
            if langCount == 3:
                lang3 = ""
                for j in Tweets:
                    if j.lang == lang[2]:
                        lang3 += j.message
                l3 = Language.get(lang[2]).display_name()
                try:
                    stopwords = nltk.corpus.stopwords.words(l3)
                except OSError:
                    stopwords = nltk.corpus.stopwords.words("english")
                results += summarise(stopwords, lang3)
        return results
    else:
        return "Error: Please check that you have not opened this page from google and that it is a valid link."


eel.start("twitter.html")
