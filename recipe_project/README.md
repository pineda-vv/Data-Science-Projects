# Recipe Project - in progress
## Business Question
* Can I build a recipe recommender system from information on the food52.com website.  As a user of the recipes on this website, I wanted to build a recommender that does not rely solely on the recipe's popularity, based on the number of likes it garners.  
---
## Data Understanding
* Data was obtained by scraping the food52 website - focusing primarily on recipes for dishes that were either "pork", "chicken", "beef" or "vegetarian" based recipe.  Using these search terms, a list of weblinks was generated and used to extract the following - recipe names, #likes, recipe ingredients, comments, from each recipe page.  Since there were no explicit user/rating pairs provided for each recipe, implicit ratings were assigned based on sentiment analysis of user comments.  
---
## Data Preparation
* A web scraper [algorithm](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/pickle_main_ingredient.py) using BeautifulSoup was optimized with the search items "chicken", "pork", "beef", or "vegetarian". Each search term generated ~200 pages with about 20 unique recipe weblinks per page.  Each list of web links was saved in a pickle file and used by a second [program](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/food52_scraper_pickleuser.py) to scrape the data.  The scraped data was saved in a mongodb database for further analysis.

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
* Sentiment analysis using nltk's Sentiment Intensity Analyzer returned a polarity score for each comment.  I used the compound score to derive implicit ratings using the following metric:

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
#### Clustering of recipe ingredients
1. Non-negative Matrix Factorization (NMF) and Latent Dirichlet Allocation (LDA) of Recipe ingredients
* Unsupervised learning using NMF and LDA was used to analyze the text of recipe ingredients and to cluster similar recipes.  Different number of clustering groups (n_components) were assessed for both model and plotted.  Subjectively, I determined that the ideal number of groups that show the best separation appear to be 6 with NMF and 4 with LDA.  Considering the recipe data was scraped using four search terms, this is not unsurprising.  The meat recipes appear to overlap quite a bit.  The other notable distinct grouping appears to be with recipes for something that require ingredients for a baked product.
* To visualize the clusters, truncated SVD(singular value decomposition) combined with t-distributed stochastic neighbor embedding(TSNE) was used for dimensionality reduction of the recipe text matrices (TF, TFidf).  The points were labeled based according to the clustering revealed by the LDA or NMF analysis.
* ##### 3-D plots of recipe groupings.
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_nmfclustering_tsne.png)

![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/3d_stack/animated_nmf.gif)


## Modeling Part 2
#### Collaborative Filtering
1. MLLib Alternating Least Squares
