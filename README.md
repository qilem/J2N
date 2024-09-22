
# Nominal Adjectives Identification

This repository contains the dataset and models for identifying nominal adjectives (JN) in text.
The models include a Hidden Markov Model (HMM), Maximum Entropy (MaxEnt) model, and a BERT-based model.
The repository also includes scripts for training and evaluating these models. Additionally, the co-reference resolution experiment can be found in the GitHub repository: [POSCorefImpact](https://github.com/DeadCardassian/POSCorefImpact).


## Table of Contents
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Models](#models)
  - [Hidden Markov Model (HMM)](#hidden-markov-model-hmm)
  - [Maximum Entropy Model (MaxEnt)](#maximum-entropy-model-maxent)
  - [BERT Model](#bert-model)
- [Usage](#usage)
  - [Dataset Preparation](#dataset-preparation)
  - [Training Models](#training-models)
  - [Evaluation](#evaluation)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Introduction
In English, a word's part of speech can vary depending on its context. This project aims to identify "nominal adjectives" (JN),
which are adjectives that function as nouns in certain contexts.
For instance, in the phrase "the poor are housed in high-rise-project apartments," the word "poor" acts as a noun.

This repository includes:
- A dataset with annotated nominal adjectives.
- Scripts for training and evaluating HMM, MaxEnt, and BERT models to identify these nominal adjectives.

## Dataset
The dataset is based on the Wall Street Journal corpus (WSJ_02-21.pos-chunk) and contains approximately 1.9 million words.
About 1,100 target words have been identified as nominal adjectives (JN). The dataset format is as follows:

- Each line consists of a word, POS tag, BIO tag, and a numerical tag indicating whether the word is a nominal adjective (0 for no, 1 for yes), separated by tabs.
- Empty lines separate sentences.

### Example:
word1 POS1 BIO1 0


## Models

### Hidden Markov Model (HMM)
The HMM model is trained to perform POS tagging with an additional tag for nominal adjectives (JN).
The model's goal is to improve tagging accuracy by correctly identifying JN words.

### Maximum Entropy Model (MaxEnt)
The MaxEnt model is another approach to POS tagging and BIO chunking, incorporating the JN tag to see if it improves chunking performance.

### BERT Model
The BERT model is fine-tuned to identify nominal adjectives in text without pre-existing POS or BIO chunk tags.
This model uses a weighted loss function to address the class imbalance of JN tags in the dataset.

## Usage

### Dataset Preparation
1. Clone the repository:
   ```bash
   git clone https://github.com/qilem/J2N.git

### Training Models
- **HMM Model:**
  ```
  python trainHMM.py <training_file> <test_file> <output_file>
  ```

- **MaxEnt Model:**
  ```
  do:
  python feature_extracting.py training.pos-chunk training.feature testing.pos test.feature

  Compile and run MEtrain.java, giving it the feature-enhanced training file as input;
  it will produce a MaxEnt model. MEtrain and MEtest use the maxent and trove packages,
  so you must include the corresponding jar files, maxent-3.0.0.jar and trove.jar, on the classpath when you compile and run.
  Assuming all java files are in the same directory, the following command-line commands will compile and run these programs --
  these commands are slightly different for posix systems (Linux or Apple), than for Microsoft Windows.

  For Linux, Apple and other Posix systems, do:
  javac -cp maxent-3.0.0.jar:trove.jar *.java ### compiling
  java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk ### creating the model of the training data
  java -cp .:maxent-3.0.0.jar:trove.jar MEtag test.feature model.chunk response.chunk ### creating the system output

  For Windows Only -- Use semicolons instead of colons in each of the above commands, i.e., the command for Windows would be:
  javac -cp "maxent-3.0.0.jar;trove.jar" *.java
  java -Xmx14g -cp ".;maxent-3.0.0.jar;trove.jar" MEtrain training.feature model.chunk
  java -cp ".;maxent-3.0.0.jar;trove.jar" MEtag test.feature model.chunk response.chunk
  ```
  
- **BERT Model:**
  ```
  python j2nrobot.py
  ```

### Evaluation
Evaluate the trained models on the test set:

- **HMM Model:**
  ```
  python score.py <model_file> <test_file>
  ```

- **MaxEnt Model:**
  ```
  python score.chunk.py <model_file> <test_file> <output_file>
  ```
### Coref Demo
  Make sure you have Spacy 3.0.0. Change iscustom in diy_spacy_coref_han_yang.py, 0 means run with default pos tagger and 1 means run with custom pos tagger. Then python 
  diy_spacy_coref_han_yang.py. Additionally, the details of co-reference resolution experiment can be found in the GitHub repository: [POSCorefImpact](https://github.com/DeadCardassian/POSCorefImpact).
  
## Future Work
Future directions for this project include:
- Exploring the impact of the JN tag on various NLP tasks such as semantic analysis, text simplification, sentiment analysis, and machine translation.
- Expanding the dataset to include more instances of nominal adjectives.
- Improving the accuracy and robustness of the nominal adjective recognition models.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.
