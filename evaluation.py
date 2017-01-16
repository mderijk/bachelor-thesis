import sys
import json
from collections import Counter

def classify_post(labels):
	frequencies = Counter(labels)
	if frequencies['tr'] >= 1 and frequencies['nl'] == 0:
		post_label = 'ml'
	elif frequencies['nl'] >= 1 and frequencies['tr'] == 0:
		post_label = 'ml'
	else:
		post_label = 'bl'
	
	return post_label

def evaluate(data_file, labels_file):
	post_labels = {'male': [], 'female': []} # post level labels (monolingual/bilingual)
	with open(data_file, encoding='utf-8') as posts, open(labels_file, encoding='utf-8') as labels:
		token_labels = [] # word level labels
		for label in labels:
			label = label.strip()
			
			if label:
				token_labels.append(label)
			elif token_labels:
				post = json.loads(posts.readline().strip())
				post_label = classify_post(token_labels)
				post_labels[post['user_gender']].append(post_label)
				token_labels = []
	
	male_frequencies = Counter(post_labels['male'])
	female_frequencies = Counter(post_labels['female'])
	male_total = sum(male_frequencies.values())
	female_total = sum(female_frequencies.values())
	total = male_total + female_total
	
	for label, frequency in male_frequencies.items():
		print('male', label, frequency, '{:.1f}%'.format(frequency / male_total * 100), sep='\t')
	
	for label, frequency in female_frequencies.items():
		print('female', label, frequency, '{:.1f}%'.format(frequency / female_total * 100), sep='\t')
	
	print('total', total, sep='\t')

def main(argv):
	if len(argv) == 3:
		evaluate(argv[1], argv[2])
	else:
		print("Usage: {} <path/to/data.jl> <path/to/data_labels.txt>".format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
