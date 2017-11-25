# vsm
Vector Space Model
The main implementations of the IR system are the two files named booleanretr.py(for Boolean retrieval) and 
vsmretr.py(for vector model).Indexing for boolean shall be done by executing boolindex.py and indexing for Vector Space Model shall be done using vsmindex.py.

Steps to execute:
1)Change the path for the documents collection and the query set in the files
2)First generate the index by executing boolindex.py and vsmindex.py.
3)Execute the main implementation files using python3 in the terminal.
4)The output will be shown on the terminal:
	a)Boolean : displays the no.of documents retrieved along with the time taken. 
	b)Vector model : displays the top 10 documents for each query along with time taken to execute queries.
  
NLTK needs to be installed
