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

* Pooled recipes exploratory data analysis (EDA)
-- The histogram for the count of 'likes' for each unique recipe (recipes with 1, 2, 3....n) appear to show a Poisson distribution.
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/latex_poisson_pmf.png)

* #### Figure 1 Ratings/#Likes Distribution
* A) All recipes and categories
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution.png)
* B) Ratings/#Likes Distribution for each category -- the 'vegetarian' category most likely include dessert, side dish, and vegetable main dish recipes.
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution_ingredients.png)

* Sentiment analysis using nltk's SentimentIntensityAnalyzer returned a polarity score for each comment.  I used the compound score to derice implicit ratings using the following metric:

| **Rating** | **Compound Score** |
|:---:|:---:|
| **3** | **> 0.6** |
| **2** | **0.3 - 0.6** |
| **1** | **0 - 0.3** |
| **0** | **<= 0** |

* The ratings distribution is shown in the following table and plot.
#### **Total count per rating category**
| **Rating** | **Counts** |
|:---:|:---:|
| **3** | **29026** |
| **2** | **8228** |
| **1** | **2115** |
| **0** | **13538** |
* 
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/implicit_dist.png)
---
## Modeling Part 1
#### Clustering of recipe ingredients
1.  Initial modeling centered on trying to build a simple predictive model on whether a recipe (~9300 collected) is "popular" or not.  Intuitively, the recipes with a rating of either 1 or 0 could have been used as the positive ('not popular') class.  However, some of these recipes are likely newly uploaded to the site and perhaps have not been seen/rated by enough viewers.  Thus, a threshold was chosen instead. Recipes with less than or equal to 10 likes were labeled as the positive class (Figure 2A)  This modeling worked well, after engineering some features based on the text of the recipes.  

2. Model Evaluation -- cross-validation metrics of popularity classifier.

* #### Figure 2
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/classifier_analysis.png)

## Modeling Part 2
#### Clustering of Recipes using non-negative matrix factorization (NMF) and t-distributed stochastic neighbor embeding (t-SNE)
1. Non-negative matrix factorization used to extract the top topics/word groups in the recipe text (ingredients) as well as the title.

![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_text_tsne.png)
