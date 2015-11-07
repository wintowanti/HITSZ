# -*- coding:UTF-8 -*-

def read_file(filename,flag):
	'''
		filename 文件名
		flag 预留删除字符
	'''
	fs = open(filename,'r')
	lines = fs.read();
	lines = lines.split("\n")
	return lines

def get_words(line):
	'''
	
	'''
	import jieba
	tmp = jieba.cut(line, cut_all=False)
	words = []
	for item in tmp:
		words.append(item)
	return words

def get_matrix(array_words):
	keys_set = set()
	for words in array_words:
		for word in words:
			if word not in keys_set:
				keys_set.add(word)
	#去除噪点信息
	dic = {}
	for item in keys_set:
		dic[item] = 0;
	for words in array_words:
		for word in words:
			if word in keys_set:
				dic[word] += 1;
	for key in dic:
		print key,"  ",dic[key]
	keys = [];
	for key in dic:
		# 剔除就出现过一次的
		if dic[key] > 0:
			keys.append(key)
	print " ".join(keys)
	keys.sort();
	print " ".join(keys)
	matrix = [];
	for words in array_words:
		vector = []
		for key in keys:
			if key in words: vector.append(1.0)
			else: vector.append(0.0)
		matrix.append(vector)
	return matrix,keys	

def get_vector(line,keys):
	words = get_words(line);
	vector = []
	for key in keys:
		if key in words: vector.append(1.0)
		else: vector.append(0.0)
	return vector

if __name__ == "__main__":
	lines = read_file("test.txt","")
	words0 = get_words(lines[0])
	words1 = get_words(lines[1])
	words2 = get_words(lines[2])
	words3 = get_words(lines[3])

	print "+".join(words0);
	print "+".join(words1);
	print "OK"

	matrix,keys = get_matrix([words0,words1,words2,words3])
	print "*".join(keys)
	test_str ="我今天老开心了。"
	vector = get_vector(test_str,keys)
	for item in vector:
		print item
