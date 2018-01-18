# Data-Science-Projects
### Repository of all data science projects I have worked on.
#### These include analyses that were part of the Galvanize DSI program as well as subsequent pet projects.  Apart from the case studies, I conceived and executed all other projects that are discussed here.

## 1. Galvanize DSI Capstone Project
* **Creating a Gene Network without prior knowledge of biology.**  I used text mining and text clustering to build a gene association network.  Once the full gene graph was built, I then used the cluster analysis to create a knowledge base that can provide journal articles that are relevant to specific gene-groups/network. Details can be found **[here.](https://github.com/pineda-vv/Creating-gene-networks-using-NLP)**


## 2. Recipe Recommender System (RS)
* #### I built two recipe recommenders with data I scraped from two popular recipe websites.  
* **Implicit ratings derived from user comments**.  In this project, I scraped data from the Food52 website where each recipe page had details about the dish (recipe, title) as well as the number of visitors who liked the recipe and some user comments.  I used text analysis(Non-negative Matrix Factorization and Latent Dirichlet Allocation) to cluster the recipes into different groups and used t-SNE dimensionality reduction to be able to visualize the clustering analyses.  I then used text sentiment analysis to derive implicit ratings based on the whether the user comment on the site was positive or negative. Details of all these analyses can be found **[here](https://github.com/pineda-vv/Data-Science-Projects/tree/master/recipe_project)**.
* **Explicit ratings provided by site users.**  In contrast to the Food52 recipe recommender system which was built with implicit ratings, I scraped the Allrecipe.com site to build an RS with explicit ratings.  Details of this work can be found **[here](https://github.com/pineda-vv/allrecipe_recommender)**.

## 3. Case Studies/Group Projects
* #### These case studies were all done utilizing CRISP-DM and pair programming.  
* **Predicting future sales at a farm equipment auction house.**  Using data from previous auctions, we used linear regression algorithms to build a model that predicts future auction prices.
* **Churn prediction** for a ride-share company.  The exercise involved a lot of exploratory data analysis, feature engineering, and creating labels for each user.  Our group chose, optimized, and cross-validated a gradient boosting classifier model and used the model's precision and recall of the test data as our performance indicators.  
* **Recommender system** - movie recommender built using collaborative filtering.  This involved implementing solutions to the cold start problem.  Built the recommender using Spark MLib Alternating Least Squares.
* **Fraud detection system** - built a classifier model to detect fraud in real time for a fictitious e-commerce company that provided event staging/ticketing.  Our group built a robust model and set appropriate probability thresholds which we then used in a dashboard to flag possible fraud on new data. Based on this screening, we also formulated actionable responses to the new information i.e. whether to have a human follow up with the posting or to shut down the posting at once.
