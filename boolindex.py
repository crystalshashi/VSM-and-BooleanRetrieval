import pickle
import glob
from nltk.stem import PorterStemmer
import os
import psutil
from timeit import default_timer

start = default_timer()
Index = {}
p = psutil.Process(os.getpid())
path = 'C:/Users/crystal/Downloads/rfcs/*.txt'
files = glob.glob(path)
ps = PorterStemmer()
sp = {'!':0,'~':0,'`':0,'@':0,'#':0,'$':0,'%':0,'^':0,'&':0,'*':0,'(':0,')':0,'-':0,'_':0,'=':0,'+':0,'{':0,'[':0,'}':0,
      ']':0,':':0,';':0,'"':0,"'":0,'<':0,'>':0,'?':0,',':0,'.':0,'/':0,'|':0,"'\'":0,"\n":0," ":0,"":0}
for file in files:
    with open(file) as newfile:
        name = os.path.basename(file)
        words = newfile.read()
        words = words.replace("\n"," ")
        words = words.replace("-"," ")
        for data in words.split(" "):
            if data not in sp:
                data = data.strip('"').lstrip('[').rstrip(']').lstrip('(').rstrip(')').lstrip('{').rstrip('}').\
                    rstrip('?').strip("'").strip('"').lower()
                data = ps.stem(data)
                if data in Index:
                    dat = Index[data]
                    dat.add(name)
                    Index[data] = dat
                else:
                    Index[data] = set(name)
print("Memory used for indexing: {0:0.3f} MB".format(p.memory_info()[0]/float(2**20)))
print("Time taken for Indexing: {0:0.3f}".format(default_timer() - start))
start = default_timer()
with open('C:/Study/AIR/Index.pickle', 'wb') as newfile:
    pickle.dump(Index, newfile)
print("Memory used to Store Index on Disk: {0:0.3f} MB".format(p.memory_info()[0]/float(2**20)))
print("Time taken to Store Index on Disk: {0:0.3f} seconds".format(default_timer() - start))
