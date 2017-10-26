# Recipe Project - in progress
## Question for this Exercise/Project
* What information can I extract from the popularity of recipes posted on the food52 website?
* Can a recipe recommender system be built with just the popularity index (number of likes) for each recipe without explicit user ratings?
---
## Data Understanding
* Data scraped from the food52 website - focusing primarily on recipes for dishes that either contain "pork", "chicken", "beef" or is "vegetarian".  Collected weblinks using those search terms and then used those links to extract the recipe titles, #likes, recipe ingredients from individual recipe pages.  Information will be extracted from the text of the recipe title and/or the recipe text itself
---
## Data Preparation
* A web scraper [algorithm](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/pickle_main_ingredient.py) using BeautifulSoup was optimized with the search items "chicken", "pork", "beef", or "vegetarian". Each search term returned ~200 pages of web links to unique recipes.  The list of web links were saved in a pickle file and used by a second [program](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/food52_scraper_pickleuser.py).  Each link opened the page for that recipe and the number of likes, recipe title, and ingredients were captured and saved in a mongodb database.

* The contents of the mongodb were extracted using this [snippet](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/recipe_src/recipe_eda.py) and saved into a csv file.  Since most of the scraping was done using an AWS EC2 instance, this facilitated transport of the data back to a local machine for analysis.

### Snapshot of captured Data


* Pooled recipes exploratory data analysis (EDA)
-- The histogram for the count of 'likes' for each unique recipe (recipes with 1, 2, 3....n) appear to show a Poisson distribution.
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/latex_poisson_pmf.png)

* #### Figure 1 Ratings Distribution
* A) All recipes and categories
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution.png)
* B) Ratings Distribution for each category -- the 'vegetarian' category most likely include dessert, side dish, and vegetable main dish recipes.
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution_ingredients.png)

---
## Modeling Part 1
#### Popularity - Using Gradient Boosting Classifier
1.  Initial modeling centered on trying to build a simple predictive model on whether a recipe (~9300 collected) is "popular" or not.  Intuitively, the recipes with a rating of either 1 or 0 could have been used as the positive ('not popular') class.  However, some of these recipes are likely newly uploaded to the site and perhaps have not been seen/rated by enough viewers.  Thus, a threshold was chosen instead. Recipes with less than or equal to 10 likes were labeled as the positive class (Figure 2A)  This modeling worked well, after engineering some features based on the text of the recipes.  

2. Model Evaluation -- cross-validation metrics of popularity classifier.

* #### Figure 2
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/classifier_analysis.png)

## Modeling Part 2
#### Clustering of Recipes using non-negative matrix factorization (NMF) and t-distributed stochastic neighbor embeding (t-SNE)
1. Non-negative matrix factorization used to extract the top topics/word groups in the recipe text (ingredients) as well as the title.

![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_text_tsne.png)
