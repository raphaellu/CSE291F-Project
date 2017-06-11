# CSE291F-Project
This repository contains files used for data pre-processing and implementations of multiple algorithms (common-neighbor, supervised machine learning, supervised random walk) targeting recommendation system using amazon dataset.

### 0. amazon-meta.txt
Please download and upzip it from this link: http://snap.stanford.edu/data/amazon-meta.html
Put it into the same directory as codes.

### 1. prepocessor.py
<br />reads 'amazon-meta.txt', outputs
- amazon-meta_item_user.txt: item [users]
- amazon-meta_user_item.txt: user [items]
- amazon-meta_item_info_csv: item info (ASIN^title^salesrank^numOfReviews^AvgRating^nth_year^nth_rating^nth_vote^nth_helpful^.....^nth_categoty....)
- amazon-meta_item_item_graph: item item 1
- amazon-meta_item_item_user: user user 1  (TO GENERATE IT: comment out line 187)

### 2. sample_groundtruth.py
<br /> Samples a fraction of data from ground truth file.
<br /> filters the ground truth data such that all involved nodes are definitely in the graph.

### 3. project data analysis.ipynb
<br />Generates properties and respective plots. Analysis included in final paper.

### 4. generate ground truth graph ML.ipynb
<br />Reads in 'amazon-meta_filtered_ground_truth.txt'
<br />Outputs 'amazon-meta_item_item_0.txt' 
<br />Generates ground truth graph for Machine Learning Approach

### 5. Common Neighbors.ipynb (Baseline algorithm)
<br />Reads in 'amazon-meta_item_item_graph.txt', 'amazon-meta_filtered_ground_truth.txt'
<br />Performs common neighbors algorithm and predict classification and recommendations

### 6. ML algorithm.ipynb (Machine Learning Approach)
<br />Reads in 'amazon-meta_filtered_ground_truth.txt', 'amazon-meta_item_item_0.txt', 'amazon-meta_item_info.csv'
<br />Extracts features from training set and performs different algorithms to predict classification and recommendations

### 7. Generate graph for SRW.ipynb
<br />Reads in 'amazon-meta_filtered_ground_truth.txt', 'amazon-meta_filtered_ground_truth.txt', 'amazon-meta_item_info.csv'
<br />Outputs 'amazon-meta_item_item_1.txt','amazon-meta_item_item_2.txt'
<br />Splits ground truth file into training and testing files

### 8. SRW.ipynb (Graph Mining Approach)
<br />Reads in 'amazon-meta_item_item_1.txt','amazon-meta_item_item_2.txt','amazon-meta_filtered_ground_truth.txt'
<br />Performs Supervised Random Walk algorithm and predict classification and recommendations

