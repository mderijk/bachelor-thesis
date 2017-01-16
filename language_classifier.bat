@setlocal enableextensions enabledelayedexpansion
@echo OFF
REM first argument should be the file path to the forum data. The file is expected to end in '.jl'.

SET source=%1
SET source=!source:~0,-3!

python crfsuite_formatter.py %source%.jl
python classifier/chunker/chunking.py < %source%.txt > %source%.crfsuite.txt

crfsuite tag -m classifier/CoNLL2000.model %source%.crfsuite.txt > %source%_labels.txt
python evaluation.py %source%.jl %source%_labels.txt
