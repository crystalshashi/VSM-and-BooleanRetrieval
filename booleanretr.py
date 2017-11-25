import pickle
import enchant
import difflib
from timeit import default_timer
from nltk.stem import PorterStemmer

with open('C:/Study/AIR/Index.pickle', 'rb') as newfile:
     Index = pickle.load(newfile)


ps = PorterStemmer()
di = enchant.Dict("en_US")
res = []
orf,andf = 0,0
i = 0
def spellcorrect(i,mstr):
    global query
    global dquery
    dd = 0
    tt = ""
    if not di.check(mstr.strip('"').lower()):
        tl = di.suggest(mstr)
        for j in tl:
            seq=difflib.SequenceMatcher(None,j,mstr)
            d=seq.ratio()*100
            if d > dd:
                tt = j
                dd = d
        query[i] = ps.stem(tt)
        dquery[i] = tt

with open('C:/Users/crystal/Downloads/boolean.txt', 'r') as newfile:
    content = newfile.readlines()
dquery = []
for query in content:
    q = []
    flag = 0
    mflag = 0
    print("Query :",query,end=" ")
    query = query.rstrip('\n').split(' ')
    start = default_timer()
    dquery = query
    for i in range(0,len(query)):
        if query[i] != "OR" and query[i] != "AND":
            term = query[i].replace("'","")
            term = term.strip('"').lstrip('[').rstrip(']').lstrip('(').rstrip(')').lstrip('{').rstrip('}').rstrip('?').strip('"').lower()
            term = ps.stem(term)
            if term not in Index:
                spellcorrect(i,query[i])
                mflag = 1
            else:
                query[i] = term
    if mflag == 1:
        print("Did you mean : ",end=' ')
        for i in dquery:
            print(i,end=' ')
    print("")

    while i <= len(query)-1:
        if query[i] == "AND":
            andf = 1
        elif query[i] == "OR":
            orf = 1
        elif orf == 1:
            if query[i] in Index:
                res.append(Index[query[i]])
            else:
                s = set()
                res.append(s)
            res[0] = res[0].union(res[1])
            res.pop()
            andf,orf = 0,0
        elif andf == 1:
            if query[i] in Index:
                res.append(Index[query[i]])
            else:
                s = set()
                res.append(s)
            res[0] = res[0].intersection(res[1])
            res.pop()
            andf,orf = 0,0
        else:
            if query[i] in Index:
                res.append(Index[query[i]])
            else:
                s = set()
                res.append(s)
            andf,orf = 0,0
        i += 1
    if res[0]:
        print("About {0} results found in ({1:0.4f} seconds)".format(len(res[0]),(default_timer() - start)))
    else:
        print("Error 404")
