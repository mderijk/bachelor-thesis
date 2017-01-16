import sys
import os
import langid

def featurize(data_path):
	os.makedirs('features', exist_ok=True)
	train = (os.path.join(data_path, 'train.txt'), 'features/train.txt')
	dev = (os.path.join(data_path, 'dev.txt'), 'features/dev.txt')
	test = (os.path.join(data_path, 'test.txt'), 'features/test.txt')
	
	langid.set_languages(['nl', 'tr', 'en'])
	
	for old, new in train, dev, test:
		with open(old, encoding='utf-8') as source, open(new, 'w', encoding='utf-8') as target:
			for line in source:
				line = line.strip()
				if line:
					label, word = line.split('\t', maxsplit=1)
					word = word.lower()
					langid_lang, _ = langid.classify(word)
					print(label, word, word[-3:], word[-2:], word[-1:], word[:1], word[:2], word[:3], langid_lang, sep='\t', file=target)
				else:
					print(file=target)

def main(argv):
	if len(argv) == 2:
		featurize(argv[1])
	else:
		print("Usage: {} path/to/nguyen_dataset/".format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
