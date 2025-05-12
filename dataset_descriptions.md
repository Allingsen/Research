# Big-Picture:
- "Dataset A": Used as training data for a classificaiton SVM, used to determine whether a post was created by an educator, student, or researcher (Target group) or not.
- "Dataset B": A collection of tweets and Bluesky posts that will be fed into the classifier trained on Dataset A. This specific dataset will grow as more posts are collected (Like the 3.9 million we have recieved recently from Abishethvarman et al)
- "Dataset C": A refinement of Dataset B that only contains posts from educators. Will (hopefully) also grow as more posts are added to Dataset B

# Dataset Name: Tagged Bluesky Posts

## Overview

### Short Name: bluesky_posts_tagged.csv

### Description: A collection of scraped Bluesky Posts, ~2000 of which have been tagged by Rana. This subset is what actually used, however the remaing posts were kept to use with other datasets (primarily dataset_1_cleaned)

### Purpose: Training data for SVM (tagged subset), agglomerate with other bluesky posts to gather as many posts as possible

## Origin

### Source: Bluesky

### Date of Collection: 6/28/23 - 10/?/25 (If needed, this date can be found)

## Composition

### Instances: 31238 (2001 tagged)

### Attributes: 9

### Feature Types: 1-6: Text 7-9: Binary

### Target: None

## Pre-processing

### Steps Taken: None

# Dataset Name: Initial Abishethvarman et al data

## Overview

### Short Name: categorized_data.csb

### Description: A collection of twitter posts collected for other insight into how people are reacting to LLMs. Tagged using the dataset_1_cleaner script, which used the given job titles to create a subset that was able to be used as training data for the SVM

### Purpose: Training data for SVM, as well as potential large amounts of new data for Sentiment Analysis (So far, only been used for training data)

## Origin

### Source: https://ieeexplore.ieee.org/document/10629351

### Date of Collection: Unknown

## Composition

### Instances: 608537 (41189 Tagged)

### Attributes: 12

### Feature Types: 1-12: Text

### Target: None

## Pre-processing

### Steps Taken: None

# Dataset Name: "Dataset B"

## Overview

### Short Name: bluesky_posts_all.csv

### Description: This is a repo of all the bluesky posts that have been collected using the bluesky_scraper script. Methodology of how this has been collected is listed there.

### Purpose: Fed in to the trained SVM to then be further refined into the educators dataset

## Origin

### Source: Bluesky

### Date of Collection: 6/28/23 - 3/27/25

## Composition

### Instances: 121617

### Attributes: 6

### Feature Types: 1-6: text

### Target: None

## Pre-processing

### Steps Taken: None

# Dataset Name: "Dataset A"

## Overview

### Short Name: dataset_1_cleaned

### Description: A collection of Twitter posts and Bluesky posts, tagged by Rana/Abishethvarman et al.

### Purpose: This dataset is a combination of the subsets listed in "Tagged Bluesky Posts" and "Initial Abishethvarman et al data", which was used to train the classification SVM.

## Origin

### Source: Bluesky/Abishethvarman et al.

### Date of Collection: Vaires (See above)

## Composition

### Instances: 42582

### Attributes: 3

### Feature Types: 1,3: Text 2: Binary

### Target: label, cat_label (Depending on classifcation technique)

## Pre-processing

### Steps Taken:
1. Combining tagged-subsets
2. Removing non-applicable columns
3. Removing values with no text

# Dataset Name: Dataset C

## Overview

### Short Name: educators.csv

### Description: A reduced version of Dataset B only comprised of our target group

### Purpose: This dataset is the "final product" of our data collection and cleaning, as it is what we perform our sentiment analysis and other NLP techniques on

## Origin

### Source: Bluesky

### Date of Collection: 6/28/23 - 3/27/25

## Composition

### Instances: 16087

### Attributes: 6

### Feature Types: 1-6: Text

### Target: label

## Pre-processing

### Steps Taken:
1. Filtered using SVM to only include educators