import pickle
import glob
from nltk.stem import PorterStemmer
import os
import psutil
from timeit import default_timer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import math

start = default_timer()
tf = {}
idf = {}
p = psutil.Process(os.getpid())
path = 'C:/Users/crystal/Downloads/rfcs/*.txt'
files = glob.glob(path)
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

doclen = 0
for file in files:
    with open(file) as newfile:
        name = os.path.basename(file)
        words = newfile.read()
        words = words.replace("\n"," ")
        words = words.replace("-"," ")
        for data in words.split(" "):
            data = data.strip('"').lstrip('[').rstrip(']').lstrip('(').rstrip(')').lstrip('{').rstrip('}'). \
                rstrip('?').rstrip('\n').strip("'").strip('"').lower()
            data = lemmatizer.lemmatize(data)

            if data in tf:
                if name not in tf[data]:
                    d1 = tf[data]
                    d1[name] = 1
                    d1["LEN"] += 1
                    tf[data] = d1
            else:
                tf[data] = {name:1,"LEN":1}
            if name in idf:
                if data in idf[name]:
                    d = idf[name]
                    d[data] += 1
                    d["LEN"] += 1
                    idf[name] = d
                else:
                    d1 = idf[name]
                    d1[data] = 1
                    d1["LEN"] += 1
                    idf[name] = d1
            else:
                idf[name] = {data:1,"LEN":1}
    doclen += 1
with open('C:/Study/AIR/ttfvsmIndex.pickle', 'wb') as newfile:
    pickle.dump(tf, newfile)
for i in tf:
    d = tf[i]
    tf[i] = 1 + math.log(doclen/d["LEN"])
for i in idf:
    for j in idf[i]:
        if j != "LEN":
            d = idf[i]
            d[j] = d[j]/d["LEN"]
            d[j] *= tf[j]
            idf[i] = d
print("Memory usage: {0:0.3f} MB".format(p.memory_info()[0]/float(2**20)))
print("Execution time for Indexing: {0:0.3f}".format(default_timer() - start))
start = default_timer()
with open('C:/Study/AIR/tfvsmIndex.pickle', 'wb') as newfile:
    pickle.dump(idf, newfile)
with open('C:/Study/AIR/idfvsmIndex.pickle', 'wb') as newfile:
    pickle.dump(tf, newfile)
print("Memory usage: {0:0.3f} MB".format(p.memory_info()[0]/float(2**20)))
print("Execution time for string Inverted Indexing: {0:0.3f}".format(default_timer() - start))
