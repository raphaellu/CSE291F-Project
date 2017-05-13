# CSE291F-Project

1. prepocessor.py
reads 'amazon-meta.txt', outputs
- amazon-meta_item_user.txt: item [users]
- amazon-meta_user_item.txt: user [items]
- amazon-meta_item_info_csv: item info (ASIN^title^salesrank^numOfReviews^AvgRating^nth_year^nth_rating^nth_vote^nth_helpful^.....^nth_categoty....)
- amazon-meta_item_item_graph: item item 1
- amazon-meta_item_item_user: user user 1  (TO GENERATE IT: comment out line 187)
