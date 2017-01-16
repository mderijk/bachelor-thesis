import sys
import os
import json
import langid

def featurize(file_path):
	langid.set_languages(['nl', 'tr', 'en'])
	
	formatted_file_path = file_path[:-3] + '.txt'
	with open(file_path, encoding='utf-8') as source, open(formatted_file_path, 'w', encoding='utf-8') as target:
		for line in source:
			post = json.loads(line.strip())
			for token in post['content']:
				token = token.lower()
				langid_lang, _ = langid.classify(token)
				print(token, token[-3:], token[-2:], token[-1:], token[:1], token[:2], token[:3], langid_lang, sep='\t', file=target)
			
			print(file=target)

def main(argv):
	if len(argv) == 2 and argv[1].endswith('.jl'):
		featurize(argv[1])
	else:
		print("Usage: {} <path/to/data.jl>".format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
