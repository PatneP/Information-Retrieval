import re
import math
import numpy as np

def buildReverseIndex(documents, reverseIndex):
	for index, document in enumerate(documents):
		for word in re.findall(r'\w+', document):
			if word not in reverseIndex:
				reverseIndex[word] = set()
			reverseIndex[word].add(index)

def buildTermIncidenceMatrix(documents,reverseIndex):
	matrix = [[0 for i in range(0, len(documents))] for i in range(0, len(reverseIndex))]
	for index, term in enumerate(sorted(reverseIndex, key=lambda s: s.lower())):
		for doc_id, document in enumerate(documents):
			match = re.findall(r'\b' + term + r'\b', document)
			if not match:
				matrix[index][doc_id] = 0
			else:
				matrix[index][doc_id] = len(match)
	return matrix

def buildTF_IDFMatrix(matrix, reverseIndex, totalDocuments):
	for i, term in enumerate(sorted(reverseIndex, key=lambda s: s.lower())):
		for j in range(0, len(matrix[0])):
			if matrix[i][j] == 0:
				matrix[i][j] = 0
			else:
				matrix[i][j] = float("{0:.4f}".format((1 + math.log10(matrix[i][j])) * (math.log10(int(totalDocuments)/len(reverseIndex[term])))))
	

def buildNormalisedMatrix(matrix):
	for j in range(0, len(matrix[0])):
		mod = 0
		for i in range(0, len(matrix)):
			mod += matrix[i][j] * matrix[i][j]
		mod = float("{0:.4f}".format(math.sqrt(mod)))
		if mod != 0:
			for i in range(0, len(matrix)):
				matrix[i][j] = float("{0:.4f}".format(matrix[i][j]/mod))
			
def cosineSimilarityComputation(matrix, doc1, doc2):
	cosine = 0
	#print(doc1)
	#print(doc2)
	for i in range(len(doc1)):
		cosine += doc1[i] * doc2[i]
	return cosine

def printTermIncidenceMatrix(matrix, reverseIndex, documents):
	for index, term in enumerate(sorted(reverseIndex, key=lambda s: s.lower())):
		print(term + ' -> ' + str(matrix[index]))


def main():
	documents = list()
	reverseIndex = {}

	print('Enter the total number of documents in the collection: ')
	totalDocuments = input()

	print('Enter the number of documents: ')
	numberOfDocuments = int(input())

	for number in range(1, numberOfDocuments + 1):
		print('Document ' + str(number) + ':')
		content = input()
		documents.append(content)

	buildReverseIndex(documents, reverseIndex)
	matrix = buildTermIncidenceMatrix(documents, reverseIndex)
	print("Term frequency Matrix:")
	printTermIncidenceMatrix(matrix, reverseIndex, documents)
	print('\n')
	buildTF_IDFMatrix(matrix, reverseIndex, totalDocuments)
	print("TF-IDF Matrix:")
	printTermIncidenceMatrix(matrix, reverseIndex, documents)
	print('\n')
	buildNormalisedMatrix(matrix)
	print("Normalised Matrix:")
	printTermIncidenceMatrix(matrix, reverseIndex, documents)
	print('\n')

	print('Finding similarity between all documents: ')
	for i in range(0, len(documents) - 1):
		for j in range(i+1, len(documents)):
			cosine_similarity = cosineSimilarityComputation(matrix, np.array(matrix)[:, i], np.array(matrix)[:, j])
			print('Doc' + str(i+1) + ' and Doc' + str(j+1) + ' : ' + str(float("{0:.4f}".format(cosine_similarity))))
		
if __name__ == '__main__':
	main()
