import nltk
import sys
import os 
import string
import math
#nltk.download('all')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    #files = load_files("corpus")
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)


    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    dictLabels= {}
  
    for file  in os.listdir(directory):
        textFile = open(os.path.join(directory,file),'r')
        text = textFile.read() 
        dictLabels.update({file:text})
        
    return dictLabels

    


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    tokens = nltk.tokenize.word_tokenize(document)
    filterTokens = []
    for word in tokens:
        if (word not in nltk.corpus.stopwords.words("english")) and (word not in list(string.punctuation)):
            filterTokens.append(word.lower())
    filterTokens.sort()
    return filterTokens
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    for doc, str in documents.items():
        words = set(str)
        for word in words:
            if word in idfs.keys():
                idfs.update({word:idfs[word]+1})
            else:
                idfs.update({word:1})

    for word, cantidad in idfs.items():
        idfs.update({word:math.log(len(documents.keys())/cantidad)})        
    return idfs
    
    

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    tf_idf = dict.fromkeys(files.keys(),0)
    words_checked = []
   
    for file, strs in files.items():
        for word in query:
            if (word in strs) and (word not in words_checked):
                tf_idf.update({file:tf_idf[file]+strs.count(word) *  idfs[word]})
                words_checked.append(word)
            words_checked = []
                
    
    orden = [x for x,y in sorted(tf_idf.items(), key=lambda item: item[1], reverse=True)]

    return orden[:n]                  
    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf = dict.fromkeys(sentences.keys(),0)
    qtd = dict.fromkeys(sentences.keys(),0)
    words_checked = []
   
    for sentence, strs in sentences.items():
        wis = 0
        for word in query:
            if (word in strs) and (word not in words_checked):
                idf.update({sentence:idf[sentence]+idfs[word]})
                wis += 1
                #qtd.update({sentence:strs.count(word)})
                words_checked.append(word)
            words_checked = []
        qtd.update({sentence:wis/len(strs)})
    
    orden = sorted(idf.keys(), key = lambda x: (idf[x],qtd[x]), reverse = True)

    return orden[:n]     
    
  


if __name__ == "__main__":
    main()
