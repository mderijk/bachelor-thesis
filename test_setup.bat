@echo OFF
REM arguments are the folder names to the source, target and chunker with standard names.

SET source=%1

python %source%/chunker/chunking.py < %source%/train.txt > %source%/train.crfsuite.txt
python %source%/chunker/chunking.py < %source%/dev.txt > %source%/dev.crfsuite.txt
python %source%/chunker/chunking.py < %source%/test.txt > %source%/test.crfsuite.txt

@echo ON
crfsuite learn -m %source%/CoNLL2000.model %source%/train.crfsuite.txt
crfsuite tag -qt -m %source%/CoNLL2000.model %source%/dev.crfsuite.txt
