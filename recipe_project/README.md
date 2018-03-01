## Recipe Project - Implicit Ratings

#### Details are in this blog. http://pineda-v.com/2018-02-24-recipe-2/

**Some Images are shown below** 

## Modeling Part 1
#### Unsupervised Clustering of recipe ingredients
1. Non-negative Matrix Factorization (NMF) and Latent Dirichlet Allocation (LDA) of Recipe ingredients
* Unsupervised learning using NMF and LDA was used to analyze the text of recipe ingredients and to cluster similar recipes.  Different number of clustering groups (n_components) were assessed for both model and plotted.  Subjectively, I determined that the ideal number of groups that show the best separation appear to be 6 with NMF and 4 with LDA.  Considering the recipe data was scraped using four search terms, this is not unsurprising.  The meat recipes appear to overlap quite a bit, possibly due to a lot of shared common ingredients(salt).  In fact, as shown in the two wordcloud images, the most common words overall in the recipe text are terms that denote measures of ingredients.  Once these and other common terms are added to the set of stopwords prior to text vectorization, the clustering becomes a little more apparent.
 ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/wordcloud_all.png)  ![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/wordcloud2.png)

* Non-negative Factorization (NMF) Analysis
* Non-animated [TSNE Plot - NMF Top Topics](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_nmfclustering_tsne.png) |
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/3d_stack/animated_nmf.gif)

* Latent Dirichlet Allocation (LDA)
* Non-animated [TSNE Plot - LDA Top Topics](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/recipe_ldalabels_tsne.png) |
![alt text](https://github.com/pineda-vv/Data-Science-Projects/blob/master/recipe_project/data/lda_stack/animated_lda.gif)
---
