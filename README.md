# Code-switching and gender in multilingual online communities (bachelor thesis)

Author: Micha de Rijk


## Requirements
A working version of Python 3.
A Windows environment is recommended for ease of use, but not strictly necessary. The batch files that are included will not work on a linux environment and would have to be rewritten.
A copy of Naoaki Okazaki's CRFsuite, available at: http://www.chokkan.org/software/crfsuite/

To acquire the data from the forum you will need scrapy:

	pip install scrapy

For evaluating code-switching in the forum data, you will need the lxml and regex package:

	pip install lxml
	pip install regex

To test and train language classifiers, you will need the dataset from Nguyen et al. (2013), which is available at: http://www.dongnguyen.nl/data-langid-emnlp2013.html
For some language classifier setups you will need the langid package:

	pip install langid

If you want to install langid on Windows, you might also have to install a Microsoft Visual C++ compiler. Which version you will need and where to get it is described here: https://wiki.python.org/moin/WindowsCompilers


## Usage
There are two main uses for the various programs: testing the various setups of the language classifier and handling and evaluating the forum data.

To test a setup for the language classifier, you would run a command such as:

```bash
	$ test_setup.bat "setups/nguyen6"
```

To get post level statistics for a language classifier setup, run a command such as:

```bash
	$ post_level_evaluation.bat "setups/nguyen6" "dev.crfsuite.txt"
```


To get the data from the forum, go into the forum folder and run the posts spider:

```bash
	$ scrapy crawl posts
```

Because retrieving the data can take several hours, we recommend the following command instead:

```bash
	$ scrapy crawl posts -s JOBDIR=crawls/posts-1
```

This way you can halt the crawler at any time by pressing Ctrl-C and resume it using the same command.


To evaluate the retrieved data use:
	
```bash
	$ preprocessing.py
	$ language_classifier.bat path/to/forum_data.jl
```


## Overview
An overview of the various commands:

```
evaluation.py				Evaluates the proportions of code-switching found in the data.
featurizer.py				Used to add features to Nguyen's data for testing different combinations of features.
post_level_evaluation.bat	Evaluates the post level accuracy and f-score for a given setup folder and test set.
```

