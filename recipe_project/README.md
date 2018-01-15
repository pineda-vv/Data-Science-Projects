# Recipe Project - Recommender System with Implicit Ratings
## Business Question
* Can I build a recipe recommender system from information on the food52.com website.  As a user of the recipes on this website, I wanted to build a recommender that does not rely solely on the recipe's popularity based on the number of likes it garners.  
---
## Data Understanding
* Data was obtained by scraping the food52 website - focusing primarily on recipes for dishes that were either "pork", "chicken", "beef" or "vegetarian" based recipe.  Using these search terms, a list of weblinks was generated and used to extract the following - recipe names, #likes, recipe ingredients, comments, from each recipe page.  Since there were no explicit user/rating pairs provided for each recipe, implicit ratings were assigned based on sentiment analysis of user comments.  
---
## Data Preparation
* A web scraper [algorithm](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/pickle_main_ingredient.py) using BeautifulSoup was optimized with the search items "chicken", "pork", "beef", or "vegetarian". Each search term generated ~200 pages with about 20 unique recipe weblinks per page.  Each list of web links was saved in a pickle file and used by a second [program](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/food52_scraper_pickleuser.py) to scrape the data.  The scraped data was saved in a mongo database.

* The contents of the mongodb were extracted using this [snippet](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/recipe_eda.py) in a jupyter notebook to generate a csv vile.  Since most of the scraping was done using an AWS EC2 instance, this facilitated transport of the data back to a local machine for analysis.

### Snapshot of captured Data
* #### Data Summary
* There were 9233 recipes where the title, ingredients, aggregated comments, #total likes.  The aggregated comments were unraveled and yielded 17733 commenters/users that provided 52907 comments.
* Pooled recipe exploratory data analysis (EDA)
-- The histogram for the count of 'likes' for each unique recipe (recipes with 1, 2, 3....n) appear to show a Poisson distribution.
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/latex_poisson_pmf.png)

* #### Number of Likes per Recipe
* A) All recipes and categories
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution.png)
* B) Ratings/#Likes Distribution for each category -- the 'vegetarian' category most likely include dessert, side dish, and vegetable main dish recipes.
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution_ingredients.png)

* #### Deriving Implicit Ratings
* The food52.com recipe site did not Sentiment analysis using nltk's Sentiment Intensity Analyzer returned a polarity score for each comment.  I used the compound score to derive implicit ratings using the following metric:

| **Rating** | **Compound Score** |
|:---:|:---:|
| **3** | **> 0.6** |
| **2** | **0 to 0.6** |
| **1** | **< 0** |
| **0** | **no comments** |

* This resulted in the implicit ratings distribution shown here.
#### **Total count per rating category**
| **Rating** | **Counts** |
|:---:|:---:|
| **3** | **26108** |
| **2** | **10123** |
| **1** | **3665** |
| **0** | **16047** |
* Implicit ratings distribution plotted
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/implicit_dist.png)

---
## Modeling Part 1
#### Unsupervised Clustering of recipe ingredients
1. Non-negative Matrix Factorization (NMF) and Latent Dirichlet Allocation (LDA) of Recipe ingredients
* Unsupervised learning using NMF and LDA was used to analyze the text of recipe ingredients and to cluster similar recipes.  Different number of clustering groups (n_components) were assessed for both model and plotted.  Subjectively, I determined that the ideal number of groups that show the best separation appear to be 6 with NMF and 4 with LDA.  Considering the recipe data was scraped using four search terms, this is not unsurprising.  The meat recipes appear to overlap quite a bit, possibly due to common ingredients.  The other notable distinct grouping appears to be with recipes for something that require ingredients for a baked product.
* This is shown in this wordcloud image. | ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/wordcloud.png)
2. Visualization -  truncated SVD(singular value decomposition) combined with t-distributed stochastic neighbor embedding(TSNE) was used for dimensionality reduction of the vectorized recipe text matrices (TF, TFidf).  x, y, and z coordinates (n_components=3) were extracted from the TSNE analysis and each coordinate set was given a label based on either the LDA or NMF analysis and plotted in a 3D scatter plot.  The plots were labeled with summary terms of the top topics from each clustering analysis
---
* Non-negative Factorization (NMF) Analysis
* Non-animated [TSNE Plot - NMF Top Topics](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_nmfclustering_tsne.png) |
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/3d_stack/animated_nmf.gif)

* Latent Dirichlet Allocation (LDA)
* Non-animated [TSNE Plot - LDA Top Topics](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_ldalabels_tsne.png) |
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/lda_stack/animated_lda.gif)
---
## Modeling Part 2
#### Collaborative Filtering
1. Spark MLLib Alternating Least Squares - The recommendation system was built using Spark's ALS model.  The method of collaborative filtering aims to predict the rating of an item by a user based on the behavior of other users that "like" or highly rate the same or similar items. In short, the model takes into account the past actions (likes/ratings/purchases/web page views) of a particular user we'll call userA. The behavior of other users who have rated or liked the same or similar items. Recommendations are based on this second set of "similar" users' inclination for items or products that UserA has not seen or rated.  
2. Evaluation of the model - The user/recipe/implicit ratings matrix was split 80/20 for use as a training and test set.  The true ratings for the test set was removed.  After training the the model, the predictions for the test set were evaluated by calculating the root mean squared error (RMSE).  The average (n=3) RMSE obtained was 1.85.  The predictions are plotted against the true ratings in the following figure. ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/preds_actual.png)
