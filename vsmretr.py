import pickle
import enchant
from timeit import default_timer
from nltk.stem import WordNetLemmatizer
import math

with open('C:/Study/AIR/tfvsmIndex.pickle', 'rb') as newfile:
    tfvsm = pickle.load(newfile)
with open('C:/Study/AIR/idfvsmIndex.pickle', 'rb') as newfile:
    idfvsm = pickle.load(newfile)
with open('C:/Study/AIR/ttfvsmIndex.pickle', 'rb') as newfile:
    ttfvsm = pickle.load(newfile)

def maxscores():
    global scores
    result = 0
    top = {}
    for i in range(0,len(scores)):
        d = scores[i]
        for j in d:
            if d[j] > result:
                result = d[j]
                p = i
                top = j
    scores.pop(p)
    return top

with open('C:/Users/crystal/Downloads/vector.txt', 'r') as newfile:
    content = newfile.readlines()
lemmatizer = WordNetLemmatizer()
scores = []
for query in content:
    start = default_timer()
    q = []
    qs = 0
    flag = 0
    mflag = 0
    scores = []
    print("query :",query)
    query = query.rstrip('\n').split(' ')
    start = default_timer()
    for i in range(0,len(query)):
        term = query[i].replace("'","")
        term = term.strip('"').lstrip('[').rstrip(']').lstrip('(').rstrip(')').lstrip('{').rstrip('}').rstrip('?').\
            rstrip('\n').strip("'").strip('"').lower()
        term = lemmatizer.lemmatize(term)
        query[i] = lemmatizer.lemmatize(term)
    noofres = 0
    td = set()
    for i in query:
        if i in ttfvsm:
            for j in ttfvsm[i]:
                if j != "LEN":
                    td.add(j)
    qtfidf = {}
    for i in query:
        if i in qtfidf:
            qtfidf[i] += 1
        else:
            qtfidf[i] = 1
    for i in qtfidf:
        qtfidf[i] /= len(query)
        if i in idfvsm:
            qtfidf[i] *= idfvsm[i]
        else:
            qtfidf[i] = 0
    for j in td:
        r1 = 0
        r2 = 0
        t1 = 0
        t2 = 0
        d = tfvsm[j]
        for i in qtfidf:
            if i in d:
                t1 += d[i]**2
            t2 += qtfidf[i]**2
        r1 = math.sqrt(t1)*math.sqrt(t2)
        for i in qtfidf:
            if i in d:
                r2 += d[i] * qtfidf[i]
        if r1 != 0 and r2 != 0:
            if r2/r1 == 1:
                qs += 1
            scores.append({j:r2/r1})
        else:
            print(0)
        if qs == 10:
            break
    if len(scores) > 10:
        for i in range(0,10):
            print(maxscores())
        print("About {0} results in ({1:0.4f} seconds)".format(10,(default_timer() - start)))
    elif len(scores) == 0:
        print("No results")
    else:
        for i in scores:
            for j in i:
                print(j)
        print("About {0} results in ({1:0.4f} seconds)".format(len(scores),(default_timer() - start)))
    print("\n")
