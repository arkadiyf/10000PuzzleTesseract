import zipfile
import os
import re
import math
import pickle
from itertools import permutations


def parse_line(line):
	return re.split("[()=\s]+", line)[:-1]

element_list = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]

def elements(word):
	word = word.lower()
	return sum([(i+1)*(len(word.split(element_list[i].lower()))-1) for i in range(len(element_list))])

score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}	

def scrabble(word):
	return sum([score[let] for let in word.lower()])

def units(word):
	return len(word)

def typewriter(word):
	return len([letter for letter in word.lower() if letter in "qwertyuiop"])

def news(word):
	word = word.lower()
	up = word.count('n') - word.count('s')
	side = word.count('e') - word.count('w')
	return round((up ** 2 + side ** 2) ** 0.5,3)

let_to_num = 	{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 
                 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12, 
                 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 
                 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26}

def midpoint(word):
	mid = add_nums(word)/2.0
	i = 0
	for letter in word.lower():
		if mid > let_to_num[letter]:
			mid -= let_to_num[letter]
			i += 1
		else:
			return round(i + mid/let_to_num[letter],3)


def add_nums(word):
	return sum([let_to_num[letter] for letter in word.lower()])

def num_perms(word):
	word = sorted(word)
	ans = math.factorial(len(word))
	last = None
	num_last = 0
	for letter in word:
		if letter == last:
			num_last += 1
		else:
			ans = ans / math.factorial(num_last)
			last = letter
			num_last = 1
	ans = ans / math.factorial(num_last)
	return ans

def my_index(word):
	if len(word) == 1:
		return 0
	else:
		ordered = sorted(word)
		first_jumps = 0
		last = None
		while ordered[0] != word[0]:
			popped = ordered.pop(0)
			if popped != last:
				first_jumps += num_perms(ordered)
				last = popped

			ordered.append(popped)
		return first_jumps + my_index(word[1:])

def index(word):
	return my_index(word) + 1

def find_func(func_name):
	if func_name=="elements":
		return elements
	if func_name=="scrabble":
		return scrabble
	if func_name=="units":
		return units
	if func_name=="typewriter":
		return typewriter
	if func_name=="news":
		return news
	if func_name=="midpoint":
		return midpoint
	if func_name=="index":
		return lambda x:my_index(x)+1
	return lambda x:""
	

def read_all_words():
	words = open("words.txt")
	funcs = {elements:{}, scrabble:{}, units:{}, typewriter:{}, news:{}, midpoint:{}, index:{}}
	i = 0
	for word in words.readlines():
		word = word.strip()
		if i % 2500 == 0:
			print(i)
		i += 1
		for func in funcs:
			val = str(func(word))
			if val not in funcs[func]:
				funcs[func][val] = set()
			funcs[func][val].add(word)
	words.close()
	return funcs

funcs = None
if os.path.isfile("pickle"):
	pickle_file = open("pickle")
	funcs = pickle.load(pickle_file)
	pickle_file.close()
else:
	funcs = read_all_words()
	pickle_file = open("pickle","wb")
	pickle.dump(funcs,pickle_file)
	pickle_file.close()

print(funcs[index]["3"])

def solve():
	output = open("output.txt","w")
	for i in range(10000):
		filename = "puzzles/puzzle%04d.txt" % i
		puz = open(filename)
		possible_answers = None
		for clue in puz.readlines()[:-1]:
			info = parse_line(clue)
			func = find_func(info[0])
			val = info[2]
			if possible_answers == None:
				lookup = None
				try:
					lookup = funcs[func][val]
				except KeyError:
					print(i,info)
					lookup = set()
				possible_answers = lookup 
			else:
				possible_answers = possible_answers.intersection(lookup)
		puz.close()

		output.write("%04d: " % i + ",".join(possible_answers) + "\n")

	output.close()
'''
examples = open("examples.txt")
for line in examples.readlines():
	info = parse_line(line)
	if len(info)>2 and str(find_func(info[0])(info[1])) != info[2]:
		print(info, find_func(info[0])(info[1]))



examples.close()
'''
