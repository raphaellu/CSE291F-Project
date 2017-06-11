""" This file pre-processes the raw amazon dataset to correct format
that we can conduct common neighbor algorithm/ supervised machine learning/
supervised random walks algorithm on """

import matplotlib.pyplot as plt
import math

item_user = {}
user_item = {}
similar_item_item = {}

# flag for category-related statistics
PRINT_ALL_CATEGORIES = False

# flag for choosing category filtering metric
USE_ANY_CATEGORY = False 

def export_ground_truth(filename):
	""" export ground truth file (similar items from dataset) """
	global similar_item_item
	with open(filename, 'w') as f:
		for item in similar_item_item:
			line = item
			for s_item in similar_item_item[item]:
				line = line + ',' + s_item
			f.write(line + '\n')
	f.close()

def export_item_user_table(filename):
	""" export a hashmap storing <item, [users]> """
	global item_user
	print "generating ", filename, " ......"
	size = len(item_user)
	count = 0

	with open(filename, 'w') as f:
		for item in item_user:
			count = count + 1
			# track the progress 
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'
			line = item
			for user in item_user[item]:
				line = line + ' ' + user
			f.write(line + '\n')
	f.close()

def export_user_item_table(filename):
	""" export a hashmap storing <user, [items]> """
	global user_item

	print "generating ", filename, " ......"
	size = len(user_item)
	count = 0
	with open(filename, 'w') as f:
		for user in user_item:
			count = count + 1
			# track the progress
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'
	 		line = user
			for item in user_item[user]:
				line = line + ' ' + item
			f.write(line + '\n')
	f.close()

def read_file(filename, wanted_categories):
	""" read the raw amazon dataset and output graph-related data """
	global item_user, user_item, similar_item_item, PRINT_ALL_CATEGORIES, USE_ANY_CATEGORY
	print "read file ", filename, " ......"
	category_count = {}

	with open(filename, 'r') as f, open(filename.split('.')[0] + '_item_info.csv', 'w') as fcsv:
		lines = f.readlines()
		num_reviews = 0
		num_category_lines = 0
		categories = set() # track all unique categories
		item_asin = ''
		customers = set() # track all unique customers of one item
		fcsv.write('ASIN^title^group^salesrank^numOfReviews^AvgRating^nth_year^nth_rating^nth_vote^nth_helpful^.....^nth_categoty....\n')
		item_csv = ''
		for line in lines:
			line = line.strip()		
			# if there are more reviews to read
			if num_reviews > 0:
				if item_asin == '':
					num_reviews = 0
					continue
				tokens = line.split()	
				customer = tokens[2]
				# record customer for this item
				customers.add(customer)
				# record item for this customer
				if customer not in user_item:
					user_item[customer] = set()	
				user_item[customer].add(item_asin)
				# decrease counter for continued reviews
				num_reviews = num_reviews - 1
				item_csv = item_csv + '^' + tokens[0].split('-')[0] + '^' + tokens[4] + '^' + tokens[6] + '^' + tokens[8] 
			
			# process category lines
			if num_category_lines > 0:
				if item_asin == '':
					num_category_lines = 0
					continue
				tokens = line.split('|')[1:]
				for tok in tokens:
					clean_tok = tok.split('[')[0]
					categories.add(clean_tok)

					if PRINT_ALL_CATEGORIES: # display all categories
						if clean_tok not in category_count:
							category_count[clean_tok] = 1
						else:
							category_count[clean_tok] = category_count[clean_tok] + 1
				num_category_lines = num_category_lines - 1
				# skip the item not belonging to targeted category
				if num_category_lines == 0:
					if not USE_ANY_CATEGORY:
						for wanted_category in wanted_categories:
							if wanted_category not in categories:
								if item_asin in similar_item_item:
									del similar_item_item[item_asin]
								item_asin = ''
								break
					else:
						find_category = False
						for wanted_category in wanted_categories:
							if wanted_category in categories:
								find_category = True
								break
						# if item has none of the categories
						if not find_category:
							if item_asin in similar_item_item:
								del similar_item_item[item_asin]
							item_asin = ''
				if 'item_asin' == '':
					continue

			# start reading info for an item
			elif line != '':
				tokens = line.split()	
				if tokens[0] == 'ASIN:':
					item_asin = tokens[1]
					item_csv = tokens[1]
				elif tokens[0] == 'group:':
					item_csv = item_csv + '^' + tokens[1]
				elif tokens[0] == 'similar:':
					if item_asin == '':
						continue
					similar_items = []
					for i in range(0, int(tokens[1])):
						similar_items.append(tokens[i+2])	
					similar_item_item[item_asin] = similar_items
				elif tokens[0] == 'reviews:':
					if item_asin == '':
						continue
					try:
						num_reviews = int(tokens[4]) # num of reviews is "downloaded"
						item_csv = item_csv + '^' + tokens[4] + '^' + tokens[-1]
					except ValueError:
						print 'reviews - error'
						print tokens
						return
				elif tokens[0] == 'discontinued':
					if item_asin in similar_item_item:
						del similar_item_item[item_asin]
					item_asin = ''
				# cases below are for csv file that stores all item info
				elif tokens[0] == 'title:':
					item_csv = item_csv + '^' + line[7:]
				elif tokens[0] == 'salesrank:':
					item_csv = item_csv + '^' + tokens[1]
				elif tokens[0] == 'categories:':
					try:
						num_category_lines = int(tokens[1])
					except ValueError:
						print 'categories - error'
						print tokens
						return
					if num_category_lines == 0:
						if item_asin in similar_item_item:
							del similar_item_item[item_asin]
						item_asin = ''
						continue

			# after reading all info for an item, re-initialize local variables
			else:
				if item_asin != '':
					item_user[item_asin] = customers
					for category in categories:
						item_csv = item_csv + '^' + category
					fcsv.write(item_csv+'\n')	
				item_asin = ''
				item_csv = ''
				categories = set()
				customers = set()
	f.close()
	fcsv.close()

	# for category-related statistical purpose
	if PRINT_ALL_CATEGORIES:
		print sorted(category_count.items(), key=lambda x: x[1])
		count_freq = {}
		for c in category_count:
			v = category_count[c]
			if v not in count_freq:
				count_freq[v] = 0
			count_freq[v] = count_freq[v] + 1
		x_count = []
		y_freq = []
		for c in count_freq:
			x_count.append(math.log(c,10))
			y_freq.append(math.log(count_freq[c],10))
		plt.plot(x_count, y_freq, 'bx')
		plt.xlabel('Category Count (log)')
		plt.ylabel('Occurrence (log)')
		plt.title('log-log Category count-occurrence graph')
		plt.show()

def form_item_item_graph(filename):
	""" construct an item-item graph based on item-user table and user-item table"""
	global item_user, user_item
	
	print "generating ", filename, " ......"
	size = len(item_user)
	count = 0
	all_edges = set()

	with open(filename, 'w') as f:
		# for every item, find all its users
		for item in item_user:
			count = count + 1
			# track progress
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'			
			users = item_user[item]
			# for every user who bought that item, find other items this user bought
			for user in users:
				other_items = user_item[user]
				for other_item in other_items:
					if item != other_item and (item + ' ' + other_item) not in all_edges and (other_item +' ' + item) not in all_edges:
						f.write(item + ' ' + other_item + ' 1' + '\n')
						all_edges.add(item + ' ' + other_item)

	f.close()

def form_user_user_graph(filename):
	""" construct a user-user graph based on item-user table and user-item table"""
	global item_user, user_item

	print "generating ", filename, " ......"
	size = len(user_item)
	count = 0	
	all_edges = set()

	with open(filename, 'w') as f:
		# for every user, find all items he/she bought
		for user in user_item:
			count = count + 1
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'	
			items = user_item[user]
			# for every item, find other users who bought this item
			for item in items:
				other_users = item_user[item]
				for other_user in other_users:
					if user != other_user and (user + ' ' + other_user) not in all_edges and (other_user +' ' + user) not in all_edges:
						f.write(user + ' ' + other_user + ' 1' + '\n')
						all_edges.add(user + ' ' + other_user)
	f.close()

if __name__ == '__main__':
	filename = 'amazon-meta.txt'

	# you can also specify multiple wanted categories in form of ['Networks','Books', 'Cats']
	# only items associated with ALL wanted categories will be filtered
	# set USE_ANY_CATEGORY to True for filtering items with ANY wanted categories
	read_file(filename, ['Publishing & Books'])  
	
	export_item_user_table(filename.split('.')[0] + '_item_user.txt')
	export_user_item_table(filename.split('.')[0] + '_user_item.txt')	
	export_ground_truth(filename.split('.')[0]+'_ground_truth.txt')
	form_item_item_graph(filename.split('.')[0] + '_item_item_graph.txt')	
	# form_user_user_graph(filename.split('.')[0] + '_user_user_graph.txt')
