# Project 1: Classification
##### NYCU Spr2022: AI Capstone [DCP1271]
Author: 0816066 官澔恩

## Contents
- I. Datasets
- II. Procedures
- III. Algorithms
- IV. Analysis
- V. Discussion
- VI. Appendix

## I. Datasets
### Public Image Dataset
Source: [Kaggle: Satellite Image Classification](https://www.kaggle.com/mahmoudreda55/satellite-image-classification)

This is a dataset from Kaggle. It contains 4 classes of satellite images, which are cloudy, desert, green, and water areas. Except there being only 1,131 images of desert area, there are 1,500 images of other classes.

### Public Non-image Dataset
Source: [Kaggle: Stellar Classification Dataset - SDSS17](https://www.kaggle.com/fedesoriano/stellar-classification-dataset-sdss17)

This is a dataset from Kaggle. It contains 100,000 stellar data with 18 attributes, one of which is the class of an object. Besides, there are 3 classes, which are galaxy, quasar, and star. What's worth noticing is that the number of each class is unbalanced. There are 59,445 galaxies, 21,594 stars, and 18,961 quasars. Thus, data augmentation is required.

### Self-made Dataset
Source: [BBC News](https://www.bbc.com/news)

I made a web scraper with Selenium and BeautifulSoup that scrapes news articles from BBC News. I chose "business", "entertainment & arts", "science & environment", and "technology" as the categories to be classified. Each of them has 50 articles, that is, 200 articles in total.

First, I collected links to the page of each category. Then, I automated the following procedures with my program. For each page, it looks for and collects links that end with the same category name of current page, but if a link directs to a video news, it will be skipped. After that, it obtains a dictionary of lists containing links to news articles of each category. Subsequently, it creates directories for each category, and fetches each article and saves it under corresponding directory.

## II. Procedures
### Outline
```mermaid
flowchart LR
    load(Data Loading)
    prep(Data Preprocessing)
    model(Model Construction)
    train(Training Model)
    test(Testing Model)

    load --> prep --> model --> train --> test
```

### Satellite Image Classification
1. Load images from each directory, and save the image data and its label (the directory's name) in two lists.
2. Reshape each image data into a one-dimensional array.
3. Split the lists into a training set and a testing set.
4. Create models with different parameters and apply 5-fold cross validation with the training set.
5. Choose the best model and apply validation with the testing set.
6. Try different models and follow step 4 and 5.

### Stellar Classification
1. Load the CSV file into a data frame of Pandas.
2. Label encode the target feature.
3. Find out the correlation coefficient between each feature with the target feature, and drop those with the absolute value of the coefficient no more than 0.02.
4. Split the data frame into a part without target feature (`data_X`) and the target feature (`data_y`).
5. One-hot encode all remaining categorical features in `data_X`.
6. Split the `data_X` and `data_y` into a training set and a testing set.
7. Randomly undersample the data of major classes in the training set to make the number of each class equal.
8. Apply PCA on the training set, and apply the transformation on both training set and testing set.
9. Scale the value of each feature in the training set into $[0, 1]$, and use the same criterion on the testing set.
10. Follow step 4 to 6 in Satellite Image Classification section.

### BBC News Classification
1. Load articles from each directory, and save the texts and its label (the directory's name) in two lists.
2. Split the lists into a training set and a testing set.
3. Tokenize the article, remove stop words from it, and vectorize it with TF-IDF of each remaining word.
4. Follow step 4 to 6 in Satellite Image Classification section.

In all the train-test-spliting steps above, I tried 2 different testing set ratio, which are $0.2$ and $0.3$.

## III. Algorithms
### K-Nearest Neighbors
I tried KNN model with 3 different $k$, which is the number of neighbors to use.
- `n_neighbors`: $5$, $10$, $15$

### Random Forest
I tried random forest model with 3 different minimum number of samples to be a leaf node.
- `min_samples_leaf`: $1$, $5$, $10$

The number of decision trees I used is 100, which is chosen by default.

### Support Vector Machine
I tried SVM model with 3 different $C$, which is a regularization parameter. The strength of the regularization is inversely proportional to it.
- `C`: $1$, $5$, $10$

The kernel I used is radial basis function, which is chosen by default.

### Multilayer Perceptron
I tried MLP model with 3 different sizes of the hidden layer.
- `hidden_layer_size`: $256$, $512$, $1024$

The model has only one hidden layer.

## IV. Analysis
### Satellite Image Classification
#### KNN
##### Testing Performance with Test Size: 0.2
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 | 0.90 | 0.88 | 0.88 | 0.87 |
| 10 | 0.90 | 0.89 | 0.89 | 0.88 |
| 15 | 0.90 | 0.88 | 0.88 | 0.88 |

##### Testing Performance with Test Size: 0.3
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 | 0.90 | 0.87 | 0.87 | 0.87 |
| 10 | 0.90 | 0.88 | 0.89 | 0.88 |
| 15 | 0.90 | 0.88 | 0.88 | 0.88 |

#### Random Forest
##### Testing Performance with Test Size: 0.2
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.94 | 0.94 | 0.94 | 0.94 |
| 5 | 0.94 | 0.93 | 0.93 | 0.93 |
| 10 | 0.93 | 0.93 | 0.93 | 0.92 |

##### Testing Performance with Test Size: 0.3
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.94 | 0.93 | 0.94 | 0.93 |
| 5 | 0.93 | 0.93 | 0.93 | 0.93 |
| 10 | 0.93 | 0.93 | 0.93 | 0.92 |

#### SVM
##### Testing Performance with Test Size: 0.2
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.91 | 0.91 | 0.91 | 0.90 |
| 5 | 0.92 | 0.92 | 0.92 | 0.91 |
| 10 | 0.92 | 0.92 | 0.92 | 0.92 |

##### Testing Performance with Test Size: 0.3
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.91 | 0.90 | 0.90 | 0.90 |
| 5 | 0.92 | 0.92 | 0.92 | 0.92 |
| 10 | 0.92 | 0.92 | 0.92 | 0.91 |

#### MLP
##### Testing Performance with Test Size: 0.2
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 | 0.87 | 0.87 | 0.86 | 0.86 |
| 512 | 0.84 | 0.82 | 0.82 | 0.82 |
| 1024 | 0.86 | 0.86 | 0.86 | 0.86 |

##### Testing Performance with Test Size: 0.3
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 | 0.87 | 0.88 | 0.87 | 0.87 |
| 512 | 0.87 | 0.87 | 0.86 | 0.86 |
| 1024 | 0.86 | 0.86 | 0.86 | 0.85 |

### Stellar Classification
#### KNN
##### Testing Performance with Test Size: 0.2
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 |  |  |  |  |
| 10 |  |  |  |  |
| 15 |  |  |  |  |

##### Testing Performance with Test Size: 0.3
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 |  |  |  |  |
| 10 |  |  |  |  |
| 15 |  |  |  |  |

#### Random Forest
##### Testing Performance with Test Size: 0.2
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 5 |  |  |  |  |
| 10 |  |  |  |  |

##### Testing Performance with Test Size: 0.3
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 5 |  |  |  |  |
| 10 |  |  |  |  |

#### SVM
##### Testing Performance with Test Size: 0.2
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 5 |  |  |  |  |
| 10 |  |  |  |  |

##### Testing Performance with Test Size: 0.3
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 5 |  |  |  |  |
| 10 |  |  |  |  |

#### MLP
##### Testing Performance with Test Size: 0.2
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 |  |  |  |  |
| 512 |  |  |  |  |
| 1024 |  |  |  |  |

##### Testing Performance with Test Size: 0.3
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 |  |  |  |  |
| 512 |  |  |  |  |
| 1024 |  |  |  |  |
- After categorical features were encoded with one-hot encoding, there becomes a large number of features; therefore, it's necessary to apply PCA transformation, or the training process takes too long.
- There are so many (100,000) data, I have to remove some outliers to speed up the training.
-

### BBC News Classification
#### KNN
##### Testing Performance with Test Size: 0.2
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 | 0.82 | 0.83 | 0.83 | 0.82 |
| 10 | 0.77 | 0.76 | 0.76 | 0.75 |
| 15 | 0.85 | 0.83 | 0.83 | 0.82 |

##### Testing Performance with Test Size: 0.3
| n_neighbors | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 5 | 0.85 | 0.85 | 0.85 | 0.85 |
| 10 | 0.88 | 0.89 | 0.88 | 0.88 |
| 15 | 0.86 | 0.87 | 0.86 | 0.87 |

#### Random Forest
##### Testing Performance with Test Size: 0.2
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.88 | 0.88 | 0.87 | 0.88 |
| 5 | 0.78 | 0.78 | 0.76 | 0.78 |
| 10 | 0.82 | 0.75 | 0.74 | 0.75 |

##### Testing Performance with Test Size: 0.3
| min_samples_leaf | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.82 | 0.82 | 0.78 | 0.77 |
| 5 | 0.75 | 0.78 | 0.73 | 0.73 |
| 10 | 0.36 | 0.59 | 0.44 | 0.48 |

#### SVM
##### Testing Performance with Test Size: 0.2
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.81 | 0.77 | 0.75 | 0.78 |
| 5 | 0.91 | 0.90 | 0.90 | 0.90 |
| 10 | 0.91 | 0.90 | 0.90 | 0.90 |

##### Testing Performance with Test Size: 0.3
| C | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 1 | 0.73 | 0.75 | 0.68 | 0.68 |
| 5 | 0.82 | 0.85 | 0.82 | 0.82 |
| 10 | 0.82 | 0.85 | 0.82 | 0.82 |

#### MLP
##### Testing Performance with Test Size: 0.2
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 | 0.90 | 0.90 | 0.90 | 0.90 |
| 512 | 0.83 | 0.83 | 0.82 | 0.82 |
| 1024 | 0.83 | 0.83 | 0.82 | 0.82 |

##### Testing Performance with Test Size: 0.3
| hidden_layer_size | Average Precision | Average Recall | Average F1-score | Accuracy |
| --- | --- | --- | --- | --- |
| 256 | 0.84 | 0.87 | 0.85 | 0.85 |
| 512 | 0.86 | 0.89 | 0.87 | 0.87 |
| 1024 | 0.86 | 0.89 | 0.87 | 0.87 |

## V. Discussion
### Are the Results What I Expected?

### Factors Affecting the Performance

### Further Experiments if Time Available

### What I have learned from the Project
- Skill of dynamic web scraping
- Preprocessing of image data
- Preprocessing of text data
- Undersampling for imbalanced data

## VI. Appendix

