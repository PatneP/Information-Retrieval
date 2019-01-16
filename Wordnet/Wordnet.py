import sys
from nltk.corpus import wordnet as wn


def printAllNouns():
	nouns = [x.name().split(".")[0] for x in wn.all_synsets('n')]
	return nouns

def findMeaningsOfWord(word):
	for i, syn in enumerate(wn.synsets(word)):
		synsets = wn.synsets(syn.lemmas()[0].name())
		for j in range(0, len(synsets)):
			print(str(j+1) + ".	" + synsets[j].definition())

def findSynonymsAndAntonymsOfWord(word):
	synonyms = list()
	antonyms = list()
	for syn in wn.synsets(word):
		for l in syn.lemmas():
			if l.name() not in synonyms:
				synonyms.append(l.name())
			if l.antonyms():
				if l.antonyms()[0].name not in antonyms:
					antonyms.append(l.antonyms()[0].name())
	print("\n")
	print("Total number of synonyms: " + str(len(synonyms)) + "\n")
	for synonym in synonyms:
		print(synonym)
	print("\n")
	print("Total number of antonyms: " + str(len(antonyms)) + "\n")
	for antonym in antonyms:
		print(antonym)

def findSimilarityBetweenTwoWords(word1, word2):
	print("Similarity between words '" + word1 + "' and '" + word2 + "': ")
	print("{:.2f}".format(wn.synset(wn.synsets(word1)[0].name()).wup_similarity(wn.synset(wn.synsets(word2)[0].name()))))

def findHyponymsAndHypernyms(word):
	hyponyms = list()
	hypernyms = list()
	co_hyponyms = list()

	for syn in wn.synsets(word):
		for hyponym in syn.hyponyms():
			if hyponym.lemmas()[0].name() not in hyponyms:
				hyponyms.append(hyponym.lemmas()[0].name())
		for hypernym in syn.hypernyms():
			if hypernym.lemmas()[0].name() not in hypernyms:
				hypernyms.append(hypernym.lemmas()[0].name())
	print("\n")
	print("Hyponyms: \n")
	for hypo in hyponyms:
		print(hypo)
	print("\n")
	print("Hypernyms: \n")
	for hyper in hypernyms:
		print(hyper)
	print("\n")

	for hypernym in hypernyms:
		for syn in wn.synsets(hypernym):
			for hyponym in syn.hyponyms():
				if hyponym.lemmas()[0].name() not in co_hyponyms:
					co_hyponyms.append(hyponym.lemmas()[0].name())
	print("Co-hyponyms: \n")
	for co in co_hyponyms:
		print(co)

def getWordsRelatedToDomain(domain):
	related_words = list()
	sports = wn.synsets(domain, pos = 'n')
	hyponymy = lambda s: s.hyponyms()

	for sport in sports:
		for synset in list(sport.closure(hyponymy)):
			if synset.lemmas()[0].name() not in related_words:
				related_words.append(synset.lemmas()[0].name())
	print("\n")
	print("Related words to '" + domain  + "':\n")
	for word in related_words:
		print(word)

def getNumberOfSensesForCategory(word, pos):
	senses = list()
	for synset in wn.synsets(word):
		words = wn.synsets(synset.lemmas()[0].name(), pos = pos)
		if len(words) != 0:
			senses.extend(word.lemmas()[0].name() for word in words)
	print("\n")
	print("Number of senses as pos='" + pos + "': \n")
	print(senses)

def main():
	print("All nouns in wordnet: \n")
	nouns = printAllNouns()
	for noun in nouns[0:10]:
		print(noun)
	print("\n")
	print("Enter the word: ")
	word = input()
	findMeaningsOfWord(word)
	findSynonymsAndAntonymsOfWord(word)
	getNumberOfSensesForCategory(word, wn.NOUN)
	getNumberOfSensesForCategory(word, wn.VERB)
	getNumberOfSensesForCategory(word, wn.ADJ)
	getNumberOfSensesForCategory(word, wn.ADV)
	print("\n")
	while(1):
		print("Enter word to find similarity with word '" + word + "': ")
		word2 = input()
		findSimilarityBetweenTwoWords(word, word2)
		print("Do you want to continue(y/n): ")
		decision = input()
		if decision == 'n':
			break
	findHyponymsAndHypernyms(word)
	getWordsRelatedToDomain('sport')

	

if __name__ == "__main__":
	main()
