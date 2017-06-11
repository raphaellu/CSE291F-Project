""" This file samples and filters a fraction of data from ground truth file for testing purpose """
""" it is necessary to do this pre-processing when the constructed graph does not contain all 
items (i.e. the data file contains nodes that are not in the constructed graph) """
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
	""" filters the ground truth file such that the ground truth file does not contain 
	nodes that are not in the constructed graph"""
	similar_item_item = {}
	count = 0;
	total = 0;
	# construct the dictionary <node, [similar nodes]>
	with open(readfile, 'r') as f:
		lines = f.readlines()
		for line in lines:
			tokens = line.strip().split(',')
			key = tokens[0]
			similar_item_item[key] = tokens[1:]
			total = total + len(tokens[1:])
	f.close()

	# only write down node and similar nodes that are keys in the dictionary
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
	# display the fraction of previously existed nodes in the graph (fraction of nodes
	# that are not removed)
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