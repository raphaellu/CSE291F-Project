from random import random

def sample_lines(readfile, writefile, sample_rate):
	''' extract <sample_rate> fraction of lines from <readfile> into <writefile>
	'''
	lines = [line for line in open(readfile) if random() <= sample_rate]
	with open(writefile, 'w') as f:
		for line in lines:
			f.write(line)
	f.close()

if __name__ == '__main__':
	filename = 'amazon-meta.txt'
	# 1st arg - readfile path
	# 2nd arg - writefile path
	# 3nd arg - fraction of lines want to extract
	sample_lines(filename.split('.')[0]+'_ground_truth.txt', 
		filename.split('.')[0]+'_sampled_ground_truth.txt',
		0.2)