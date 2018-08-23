from app import idioms
import random

# Quiz
def quiz(line):
	count = 0 
	tmp = ''
	spacelist = []
	for i in range(0,len(line)):
		if line[i] == ' ':
			count += 1 
			spacelist.append(i)

	if count == 1:
		idx = line.index(' ')
		for i in range(0, idx+2):
			tmp += line[i]

		for i in range(idx+2, len(line)):
			tmp += '_'

	else:
		idx = spacelist[-1]
		tmp2 = line[:idx+2]

		for i in range(idx+2, len(line)):
			tmp2 += '_'

		return tmp2

	return tmp


rand = ['idioms_usa', 'idioms_uk']

def get_line():
	select = random.choice(rand)
	if select == 'idioms_usa':
		line = random.choice(idioms.idioms_usa)

	else:
		line = random.choice(idioms.idioms_uk)

	while(1):
		count = 0

		for char in line:
			if char == '(':
				count += 1

		if count >= 2 and select == 'idioms_usa':
			line = random.choice(idioms.idioms_usa)
		elif count >= 2 and select == 'idioms_uk':
			line = random.choice(idioms.idioms_uk)
		else:
			return line


def modify_line(line):
	if '(' in line:
		idx1 = line.index('(')
		idx2 = line.index(')')

		tmp1 = line[:idx1]
		tmp2 = line[idx2+2:]

		line = tmp1 + tmp2

	line = line.lstrip()
	line = line.rstrip()

	return line
