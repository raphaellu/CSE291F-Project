item_user = {}
user_item = {}
similar_item_item = {}


def export_item_user_table(filename):
	global item_user
	print "generating ", filename, " ......"
	size = len(item_user)
	count = 0

	with open(filename, 'w') as f:
		for item in item_user:
			count = count + 1
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'
			line = item
			for user in item_user[item]:
				line = line + ' ' + user
			f.write(line + '\n')
	f.close()

def export_user_item_table(filename):
	global user_item

	print "generating ", filename, " ......"
	size = len(user_item)
	count = 0
	with open(filename, 'w') as f:
		for user in user_item:
			count = count + 1
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'
	 		line = user
			for item in user_item[user]:
				line = line + ' ' + item
			f.write(line + '\n')
	f.close()

def read_file(filename, group):
	global item_user, user_item, similar_item_item
	print "read file ", filename, " ......"

	with open(filename, 'r') as f, open(filename.split('.')[0] + '_item_info.csv', 'w') as fcsv:
		lines = f.readlines()
		num_reviews = 0
		num_category_lines = 0
		categories = set()
		item_asin = ''
		customers = set()
		fcsv.write('ASIN^title^salesrank^numOfReviews^AvgRating^nth_year^nth_rating^nth_vote^nth_helpful^.....^nth_categoty....\n')
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
					categories.add(tok)
				num_category_lines = num_category_lines - 1


			# start reading info for an item
			elif line != '':
				tokens = line.split()	
				if tokens[0] == 'ASIN:':
					item_asin = tokens[1]
					item_csv = tokens[1]
				elif tokens[0] == 'group:':
					if tokens[1] != group:
						item_asin = ''
						item_csv = ''
						continue
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
					item_asin = ''
				# cases below are for csv file
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

def form_item_item_graph(filename):
	global item_user, user_item
	
	print "generating ", filename, " ......"
	size = len(item_user)
	count = 0

	with open(filename, 'w') as f:
		for item in item_user:
			count = count + 1
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'			
			users = item_user[item]
			for user in users:
				other_items = user_item[user]
				for other_item in other_items:
					f.write(item + ' ' + other_item + ' 1' + '\n')
	f.close()

def form_user_user_graph(filename):
	global item_user, user_item

	print "generating ", filename, " ......"
	size = len(user_item)
	count = 0

	with open(filename, 'w') as f:
		for user in user_item:
			count = count + 1
			if count % 1000 == 0:
				print (100*count/float(size)),'% finished...'	
			items = user_item[user]
			for item in items:
				other_users = item_user[item]
				for other_user in other_users:
					f.write(user + ' ' + other_user + ' 1' + '\n')
	f.close()

if __name__ == '__main__':
	filename = 'amazon-meta.txt'
	read_file(filename, 'Music')	
	export_item_user_table(filename.split('.')[0] + '_item_user.txt')
	export_user_item_table(filename.split('.')[0] + '_user_item.txt')	
	form_item_item_graph(filename.split('.')[0] + '_item_item_graph.txt')	
	# form_item_item_graph(filename.split('.')[0] + '_user_user_graph.txt')		