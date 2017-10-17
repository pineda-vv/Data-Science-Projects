# Recipe Project - in progress
## Business Question
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


* Pooled recipes
-- The histogram for Number of "Likes" per Recipe (unique) appear to show a Poisson distribution.
* ($\lambda = 1$) &nbsp;&nbsp;
$pmf = \frac{\lambda^ke^{-\lambda}}{k!}$  

![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution.png)
* Ratings Distribution for each category
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/distribution_ingredients.png)

---
## Modeling
* Initial modeling centered on
