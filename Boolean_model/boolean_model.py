import re

def AND_operation(postings1, postings2):
	return (postings1 & postings2)

def OR_operation(postings1, postings2):
	return (postings1 | postings2)

def NOT_operation(postings, universalSet):
	return (universalSet - postings)

def buildReverseIndex(documents, reverseIndex):
	for index, document in enumerate(documents):
		for word in re.findall(r'\w+', document):
			if word not in reverseIndex:
				reverseIndex[word] = set()
			reverseIndex[word].add(index)

def printReverseIndex(reverseIndex):
	for element in sorted(reverseIndex.keys(), key=lambda s: s.lower()):
		print('(' + element + ', ' + str(len(reverseIndex[element])) + ')' + ' -> ' + str(reverseIndex[element]))

def processQuery(inputQuery, reverseIndex, universalSet):
	answer = list()
	inputQuery = inputQuery.replace('not ', 'not_')
	if inputQuery[0] != '(':
		inputQuery = '(' + inputQuery + ')'
		
	bracket_results = dict()
	counter_for_brackets = 0

	regex_for_brackets = re.compile(r'\([\w\s]+\)')
	
	while True:
		match = regex_for_brackets.search(inputQuery)
		if match == None:
			break
		bracket = solveBracket(str(match.group())[1: len(str(match.group())) - 1].split(' '), universalSet, reverseIndex, bracket_results)
		bracket_results['bracket_result'+str(counter_for_brackets)] = bracket
		inputQuery = inputQuery.replace(match.group(), 'bracket_result' + str(counter_for_brackets))
		counter_for_brackets += 1
	return bracket_results[inputQuery]

def solveBracket(internal_query, universalSet, reverseIndex, bracket_results):
	if 'bracket_result' in internal_query[0]:
		result = bracket_results[internal_query[0].strip()]
	else:
		if 'not_' in internal_query[0]:
			result = universalSet - reverseIndex[internal_query[0].replace('not_', '').strip()]
		else:
			result = reverseIndex[internal_query[0]]
	for i in range(1, len(internal_query) - 1, 2):
		operator = internal_query[i]
		operand2 = internal_query[i + 1]
		if 'bracket_result' in operand2:
			term2 = bracket_results[operand2.strip()]
		elif 'not_' in operand2:
			term2 = universalSet - reverseIndex[operand2.replace('not_', '').strip()]
		else:
			term2 = reverseIndex[operand2]
		if operator == "and":
			result = AND_operation(result, term2)
		elif operator == "or":
			result = OR_operation(result, term2)
	return result



def main():
	documents = list()
	reverseIndex = {}

	print('Enter the total number of documents in the collection:')
	totalDocuments = int(input())

	universalSet = set()
	for i in range(1, totalDocuments + 1):
		universalSet.add(i)
		
	number_of_documents = totalDocuments

	for number in range(1, number_of_documents + 1):
		print('Document ' + str(number) + ':')
		content = input()
		documents.append(content)

	buildReverseIndex(documents, reverseIndex)
	printReverseIndex(reverseIndex)

	print('Enter Queries (and/or/not). Press Ctrl-D to stop querying')
	while True:
		try:
			inputQuery = input()
			if inputQuery:
				answer = processQuery(inputQuery, reverseIndex, universalSet)
				print(answer)
		except EOFError:
			break




if __name__ == '__main__':
	main()
