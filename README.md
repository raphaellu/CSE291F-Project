# CSE291F-Project

1. prepocessor.py
reads 'amazon-meta.txt', outputs
- amazon-meta_item_user.txt: item [users]
- amazon-meta_user_item.txt: user [items]
- amazon-meta_item_info_csv: item info (ASIN^title^salesrank^numOfReviews^AvgRating^nth_year^nth_rating^nth_vote^nth_helpful^.....^nth_categoty....)
- amazon-meta_item_item_graph: item item 1
- amazon-meta_item_item_user: user user 1  (TO GENERATE IT: comment out line 187)

2. sample_groundtruth.py

3. project data analysis.ipynb
Generate properties and respective plots. Analysis included in final paper.

4. generate ground truth graph.ipynb
Reads in 'amazon-meta_filtered_ground_truth.txt'
Outputs 'amazon-meta_item_item_0.txt' 
Generate ground truth graph for Machine Learning Approach

5. Common Neighbors.ipynb (Baseline algorithm)
Reads in 'amazon-meta_item_item_graph.txt', 'amazon-meta_filtered_ground_truth.txt'
Performs common neighbors algorithm and predict classification and recommendations

6. Generic model.ipynb (Machine Learning Approach)
Reads in 'amazon-meta_filtered_ground_truth.txt', 'amazon-meta_item_item_0.txt', 'amazon-meta_item_info.csv'
Extracting features from training set and performs different algorithms to predict classification and recommendations


