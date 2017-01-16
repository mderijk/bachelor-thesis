import sys
import json

def inspect(data_file, labels_file):
	with open(data_file, encoding='utf-8') as posts, open(labels_file, encoding='utf-8') as labels, open('inspect_labels.txt', 'w', encoding='utf-8') as target:
		token_labels = [] # word level labels
		for label in labels:
			label = label.strip()
			
			if label:
				token_labels.append(label)
			elif token_labels:
				post = json.loads(posts.readline().strip())
				for token, label in zip(post['content'], token_labels):
					print(token, label, sep='\t', file=target)
				print(file=target)
				token_labels = []

def main(argv):
	if len(argv) == 3:
		inspect(argv[1], argv[2])
	else:
		print("Usage: {} <path/to/data.jl> <path/to/data_labels.txt>".format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
