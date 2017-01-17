@echo OFF
REM the first argument should the path to a setup folder. The second argument should be the path to a folder containing Nguyen's dataset.

SET setup=%1
SET dataset=%2

python %setup%/featurizer.py %dataset% %setup%
python %setup%/chunker/chunking.py < %setup%/features/train.txt > %setup%/features/train.crfsuite.txt
python %setup%/chunker/chunking.py < %setup%/features/dev.txt > %setup%/features/dev.crfsuite.txt
python %setup%/chunker/chunking.py < %setup%/features/test.txt > %setup%/features/test.crfsuite.txt

crfsuite learn -m %setup%/CoNLL2000.model %setup%/features/train.crfsuite.txt
crfsuite tag -qt -m %setup%/CoNLL2000.model %setup%/features/dev.crfsuite.txt
