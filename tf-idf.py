import re
import math

def calculate_idf(documents, word):
    N = len(documents)
    count_docs_with_word = sum(1 for doc in documents if word in doc)
    return -math.log(count_docs_with_word / N)

def calculate_tf(document, word):
    words = re.split(r'\W+', document.lower())
    return words.count(word) / len(words)

def calculate_tfidf(query, document, documents):
    score = 0
    for word in re.split(r'\W+', query.lower()):
        idf = calculate_idf(documents, word)
        tf = calculate_tf(document, word)
        score += idf * tf
    return score

def process_query(query, mode, documents):
    query_words = set(re.split(r'\W+', query.lower()))
    relevant_docs = []
    for docid, document in enumerate(documents):
        if mode == "AND" and all(word in document.lower() for word in query_words):
            relevant_docs.append((docid, document))
        elif mode == "OR" and any(word in document.lower() for word in query_words):
            relevant_docs.append((docid, document))
    relevant_docs.sort(key=lambda x: calculate_tfidf(query, x[1], documents), reverse=True)
    return relevant_docs

def main():
    N = int(input())
    documents = [input() for _ in range(N)]
    M = int(input())
    for _ in range(M):
        K, mode, query = input().split('\t')
        K = int(K)
        relevant_docs = process_query(query, mode, documents)
        for i, (docid, document) in enumerate(relevant_docs[:K]):
            snippet = document[:50] + "..." if len(document) > 50 else document
            score = calculate_tfidf(query, document, documents)
            print(f"{query}\t{docid}\t{score}\t{snippet}")

if __name__ == "__main__":
    main()