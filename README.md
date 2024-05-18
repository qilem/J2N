Nominal Adjectives Identification
This repository contains the dataset and models for identifying nominal adjectives (JN) in text. The models include a Hidden Markov Model (HMM), Maximum Entropy (MaxEnt) model, and a BERT-based model. The repository also includes scripts for training and evaluating these models.

Table of Contents
Introduction
Dataset
Models
Hidden Markov Model (HMM)
Maximum Entropy Model (MaxEnt)
BERT Model
Usage
Dataset Preparation
Training and Evaluating Models
Future Work
Contributing
License
Introduction
In English, a word's part of speech can vary depending on its context. This project aims to identify "nominal adjectives" (JN), which are adjectives that function as nouns in certain contexts. For instance, in the phrase "the poor are housed in high-rise-project apartments," the word "poor" acts as a noun.

This repository includes:

A dataset with annotated nominal adjectives.
Scripts for training and evaluating HMM, MaxEnt, and BERT models to identify these nominal adjectives.
Dataset
The dataset is based on the Wall Street Journal corpus (WSJ_02-21.pos-chunk) and contains approximately 1.9 million words. About 1,100 target words have been identified as nominal adjectives (JN). The dataset format is as follows:

Each line consists of a word, POS tag, BIO tag, and a numerical tag indicating whether the word is a nominal adjective (0 for no, 1 for yes), separated by tabs.
Empty lines separate sentences.
Example:

word1    POS1    BIO1    0
word2    POS2    BIO2    0
word3    POS3    BIO3    1

word4    POS4    BIO4    0
Models
Hidden Markov Model (HMM)
The HMM model is trained to perform POS tagging with an additional tag for nominal adjectives (JN). The model leverages the Viterbi algorithm to predict tags for each word in a sentence. It handles out-of-vocabulary (OOV) items by applying heuristic rules based on word patterns—such as capitalization and common suffixes—to assign probable tags, thereby enhancing its ability to accurately tag words not encountered during training.

Training and Running the HMM Model
To run the part-of-speech tagging system with the HMM model:

bash

python trainHMM.py <training_file> <test_file> <output_file>
Replace <training_file>, <test_file>, and <output_file> with the paths to your training data, test sentences, and desired output file, respectively.

Maximum Entropy Model (MaxEnt)
The MaxEnt model uses feature extraction from the dataset to perform POS tagging and BIO chunking. It creates two output files: a training feature file from the training corpus and a test feature file from the development corpus.

Feature Extraction
To extract features from the dataset:

bash

python feature_extracting.py training.pos-chunk training.feature testing.pos test.feature
Training and Running the MaxEnt Model
For Linux, Apple, and other POSIX systems:

bash

javac -cp maxent-3.0.0.jar:trove.jar *.java
java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk
java -cp .:maxent-3.0.0.jar:trove.jar MEtag test.feature model.chunk response.chunk
For Windows:

bash

javac -cp "maxent-3.0.0.jar;trove.jar" *.java
java -Xmx14g -cp ".;maxent-3.0.0.jar;trove.jar" MEtrain training.feature model.chunk
java -cp ".;maxent-3.0.0.jar;trove.jar" MEtag test.feature model.chunk response.chunk
Scoring
To score the MaxEnt model:

bash

python score.chunk.py key.pos-chunk response.chunk
BERT Model
The BERT model is fine-tuned to identify nominal adjectives in text without pre-existing POS or BIO chunk tags. This model uses a weighted loss function to address the class imbalance of JN tags in the dataset.

Training and Running the BERT Model
To train the BERT model:

bash

python train_bert.py --dataset path/to/dataset --epochs 10 --batch_size 16
To evaluate the BERT model:

bash

python evaluate_bert.py --model path/to/trained_bert_model --dataset path/to/test_dataset
Future Work
Future directions for this project include:

Exploring the impact of the JN tag on various NLP tasks such as semantic analysis, text simplification, sentiment analysis, and machine translation.
Expanding the dataset to include more instances of nominal adjectives.
Improving the accuracy and robustness of the nominal adjective recognition models.
Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.
