#!/usr/bin/env python

"""
A feature extractor for chunking.
Copyright 2010,2011 Naoaki Okazaki.
"""

# Separator of field values.
separator = '\t'

# Field names of the input data.
fields = 'w suffix3 suffix2 suffix1 prefix1 prefix2 prefix3 langid'

# Attribute templates.
templates = (
	(('w', -2), ),
	(('w', -1), ),
	(('w',  0), ),
	(('w',  1), ),
	(('w',  2), ),
	(('w', -1), ('w',  0)),
	(('w',  0), ('w',  1)),
	(('suffix1',  0), ),
	(('suffix2',  0), ),
	(('suffix3',  0), ),
	(('prefix1',  0), ),
	(('prefix2',  0), ),
	(('prefix3',  0), ),
	(('langid',  0), ),
)


import crfutils

def feature_extractor(X):
	# Apply attribute templates to obtain features (in fact, attributes)
	crfutils.apply_templates(X, templates)
	if X:
	# Append BOS and EOS features manually
		X[0]['F'].append('__BOS__')     # BOS feature
		X[-1]['F'].append('__EOS__')    # EOS feature

if __name__ == '__main__':
	crfutils.main(feature_extractor, fields=fields, sep=separator)
