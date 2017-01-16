@echo OFF

SET source=%1
SET testset=%2

crfsuite tag -r -m %source%/CoNLL2000.model %source%/%testset% | python post_level_evaluation.py %source% %testset%
