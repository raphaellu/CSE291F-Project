from random import random

def sample_lines(readfile, writefile, sample_rate):
	''' extract <sample_rate> fraction of lines from <readfile> into <writefile>
	'''
	lines = [line for line in open(readfile) if random() <= sample_rate]
	with open(writefile, 'w') as f:
		for line in lines:
			f.write(line)
	f.close()

def check_existing_rate(readfile, writefile):
	similar_item_item = {}
	count = 0;
	total = 0;
	with open(readfile, 'r') as f:
		lines = f.readlines()
		for line in lines:
			tokens = line.strip().split(',')
			key = tokens[0]
			similar_item_item[key] = tokens[1:]
			total = total + len(tokens[1:])
	f.close()

	with open(writefile, 'w') as f:
		for key in similar_item_item:
			line = key;
			other_items = similar_item_item[key]
			for other in other_items:
				if other in similar_item_item:
					count = count + 1
					line = line + ',' + other
			f.write(line + '\n')
	f.close()
	print 'existing rate: ', count/float(total)

if __name__ == '__main__':
	filename = 'amazon-meta.txt'
	# 1st arg - readfile path
	# 2nd arg - writefile path
	# 3nd arg - fraction of lines want to extract
	sample_lines(filename.split('.')[0]+'_ground_truth.txt', 
		filename.split('.')[0]+'_sampled_ground_truth.txt',
		0.2)

	check_existing_rate(filename.split('.')[0]+'_ground_truth.txt',
		filename.split('.')[0]+'_filtered_ground_truth.txt')