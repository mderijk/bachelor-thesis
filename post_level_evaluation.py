import sys
from collections import defaultdict, Counter

def load():
	posts = []
	post = []
	for line in sys.stdin:
		line = line.strip()
		if line:
			real, predicted = line.split('\t')
			post.append((real, predicted))
		elif post:
			posts.append(post)
			post = []
	
	if post:
		posts.append(post)
	
	posts = [post for post in posts if post]
	
	return posts

def display_matrix(confusion_matrix):
	labels = sorted(confusion_matrix.keys())
	print('\t'.join([''] + labels))
	for label, predicted in sorted(confusion_matrix.items()):
		print(label, '\t'.join(str(count) for label, count in sorted(predicted.items())), sep='\t')

def evaluate_word_level(posts):
	labels = [(real, predicted) for post in posts for real, predicted in post]
	evals = [int(real == predicted) for real, predicted in labels]
	accuracy = sum(evals) / len(evals)
	
	confusion_matrix = defaultdict(lambda: defaultdict(int))
	for real, predicted in labels:
		confusion_matrix[real][predicted] += 1
	
	print('', 'precision', 'recall', sep='\t')
	for real, predictions in confusion_matrix.items():
		correct = predictions[real]
		predicted_count = sum(predictions[real] for _, predictions in confusion_matrix.items())
		real_count = sum(predictions.values())
		
		precision = correct / predicted_count
		recall = correct / real_count
		
		print(real, '{:.3f}'.format(precision), '{:.3f}'.format(recall), sep='\t')
	
#	display_matrix(confusion_matrix)
	print('accuracy (overall, including skip labels):', accuracy)

def evaluate_bilingual_accuracy(posts):
	# gather post level labels
	post_level_predictions = []
	for post in posts:
		real, predicted = zip(*post)
		real_frequencies = Counter(real)
		predicted_frequencies = Counter(predicted)
#		total = sum(counter.values())
		if real_frequencies['tr'] >= 1 and real_frequencies['nl'] >= 1:
			real_post_label = 'bl'
		elif real_frequencies['tr'] >= 1 or real_frequencies['nl'] >= 1:
			real_post_label = 'ml'
		else:
			print('Unclassifiable post:', post)
			continue
		
		if predicted_frequencies['tr'] >= 1 and predicted_frequencies['nl'] >= 1:
			predicted_post_label = 'bl'
		else:
			predicted_post_label = 'ml'
		
		post_level_predictions.append((real_post_label, predicted_post_label))
	
	# evaluate post level accuracy and f-score
	evals = [int(real == predicted) for real, predicted in post_level_predictions if real != 'skip']
	accuracy = sum(evals) / len(evals)
	
	confusion_matrix = defaultdict(lambda: defaultdict(int))
	for real, predicted in post_level_predictions:
		confusion_matrix[real][predicted] += 1
	
	f_scores = {}
	for real, predictions in confusion_matrix.items():
		correct = predictions[real]
		predicted_count = sum(predictions[real] for _, predictions in confusion_matrix.items())
		real_count = sum(predictions.values())
		
		precision = correct / predicted_count
		recall = correct / real_count
		f_score = 2 * precision * recall / (precision + recall)
		f_scores[real] = f_score
	
	f_score = sum(f_scores.values()) / len(f_scores)
	
#	display_matrix(confusion_matrix)
	print("ML/BL post level accuracy:", accuracy)
	print("ML/BL post level f-score:", f_score)

def evaluate():
	posts = load()
	print("Amount of posts:", len(posts))
	
	evaluate_word_level(posts)
	
	evaluate_bilingual_accuracy(posts)

def main(argv):
	if len(argv) == 3:
		evaluate()
	else:
		print("Usage: post_level_evaluation.bat <setupFolder> <dev/test file>".format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
