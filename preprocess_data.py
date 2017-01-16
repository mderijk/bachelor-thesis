import json
import urllib.parse
from collections import defaultdict
import random
import lxml.html
from tinytokenizer import TinyTokenizer

def clean_html(blockquote):
	tokens = []
	
	text = (blockquote.text or '').strip()
	tokens.append(text)
	
	for element in blockquote:
		if 'bbcode_container' in element.classes or element.tag == 'iframe':
			pass
		elif element.tag == 'img':
			if 'inlineimg' in element.classes:
				tokens.append('[SMILEY:{0}]'.format(element.get('title')))
			else:
				src = urllib.parse.quote(element.get('src'), safe=':/')
				tokens.append('[img src=\'{0}\']'.format(src))
		elif element.tag == 'b':
			username = element.xpath('u/a/text()')
			if username:
				bold_tail = (element.tail or '').strip()
				tokens.append('HABABAM_USER_' + username[0].replace(' ', '_'))
				tokens.append(bold_tail)
			else:
				tokens.extend(('[b]', clean_html(element), '[/b]'))
		elif element.tag == 'u':
			tokens.extend(('[u]', clean_html(element), '[/u]'))
		elif element.tag == 'i':
			tokens.extend(('[i]', clean_html(element), '[/i]'))
		elif element.tag == 'object':
			src = element.get('data')
			if not src:
				src = element.xpath('.//embed')[0].get('src')
			escaped_src = urllib.parse.quote(src, safe=':/')
			tokens.append('[object src=\'{0}\']'.format(escaped_src))
		elif element.tag in ('ol', 'ul'):
			items = element.xpath('.//li')
			for item in items:
				item_text = (item.text or '').strip()
				tokens.append(item_text)
		else:
			tokens.append(clean_html(element))
		
		tail = (element.tail or '').strip()
		tokens.append(tail)
	
	tokens = (token for token in tokens if token)
	return ' '.join(tokens)

def clean(post):
	# clean post content
	element = lxml.html.fromstring(post['content'])
	text = clean_html(element)
	post['content'] = text.replace('@ HABABAM_USER_', 'HABABAM_USER_')
	
	# clean gender labels
	if post['user_gender'] == 'images/misc/gender_Vrouw.gif':
		post['user_gender'] = 'female'
	else:
		post['user_gender'] = 'male'
	
	# clean post id
	post['id'] = post['id'].replace('post_', '')

def sample(posts, k=50):
	posts_by_subforum_and_gender = defaultdict(lambda: {'male': [], 'female': []})
	for post in posts:
		posts_by_subforum_and_gender[post['category']][post['user_gender']].append(post)
	
	sample = []
	for subforum, posts_by_gender in posts_by_subforum_and_gender.items():
		for gender, posts in posts_by_gender.items():
			if len(posts) >= k:
				sample.extend(random.sample(posts, k))
			else:
				print('WARNING: the maximum number of posts in subforum', subforum, 'for gender', gender, 'is', str(len(posts)) + '. No sample from this group was taken.')
	
	return sample

def main():
	# load
	with open('forum/forum_data.jl', encoding='utf-8') as source:
		posts = [json.loads(line.strip()) for line in source]
	
	# cleaning
	for post in posts:
		clean(post)
	posts = [post for post in posts if post['content']] # discard empty posts
	
	with open('forum/forum_data_cleaned.jl', 'w', encoding='utf-8') as target:
		for post in posts:
			print(json.dumps(post), file=target)
	
	# sampling
	posts = sample(posts, k=200) # 200 * 2 genders * 29 subforums = 11600 posts
	
	# tokenization
	tt = TinyTokenizer()
	for post in posts:
		post['content'] = tt.tokenize(post['content'])
	
	# save
	with open('forum/forum_data_sampled.jl', 'w', encoding='utf-8') as target:
		for post in posts:
			print(json.dumps(post), file=target)

if __name__ == '__main__':
	main()
