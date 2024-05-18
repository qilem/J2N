from collections import defaultdict
import sys
transition_counts = defaultdict(lambda: defaultdict(int))
emission_counts = defaultdict(lambda: defaultdict(int))
tag_counts = defaultdict(int)
if len(sys.argv) != 4:
    print("Usage: python your_script.py <training_file> <test_file> <output_file>")
    sys.exit(1)

training_file_path = sys.argv[1]
test_file_path = sys.argv[2]
output_file_path = sys.argv[3]

previous_tag = "<START>"

with open(training_file_path, "r") as file:
    for line in file:
        line = line.strip()
        if line:
            word, tag = line.split("\t")
            emission_counts[tag][word] += 1
            tag_counts[tag] += 1
            transition_counts[previous_tag][tag] += 1
            previous_tag = tag
        else:
            transition_counts[previous_tag]["<END>"] += 1
            previous_tag = "<START>"

transition_probabilities = {}
for prev_tag in transition_counts:
    transition_probabilities[prev_tag] = {}
    total_transitions = sum(transition_counts[prev_tag].values())
    for tag in transition_counts[prev_tag]:
        transition_probabilities[prev_tag][tag] = transition_counts[prev_tag][tag] / total_transitions


emission_probabilities = {}
for tag in emission_counts:
    emission_probabilities[tag] = {}
    total_emissions = sum(emission_counts[tag].values())
    for word in emission_counts[tag]:
        emission_probabilities[tag][word] = emission_counts[tag][word] / total_emissions

def get_unknown_word_tag(word):
    if word[0].isupper():
        return "NNP"
    elif word.endswith("ing"):
        return "VBG"
    elif word.endswith("ed"):
        return "VBD"
    elif word.endswith("lly"):
        return "RB"
    elif word.endswith("est"):
        return "JJS"
    else:
        return "NN"


def viterbi_algorithm(words, transition_probabilities, emission_probabilities, tag_counts):
    states = list(tag_counts.keys())
    start_prob = 1.0 / len(states)


    V = [{}]
    path = {}


    for tag in states:
        emission_prob = emission_probabilities[tag].get(words[0], 0.0) or (1e-6 if tag == get_unknown_word_tag(words[0]) else 0.0)
        V[0][tag] = transition_probabilities["<START>"].get(tag, start_prob) * emission_prob
        path[tag] = [tag]

    for i in range(1, len(words)):
        V.append({})
        new_path = {}

        for current_tag in states:
            (prob, state) = max(
                (V[i - 1][prev_tag] *
                 transition_probabilities[prev_tag].get(current_tag, 1e-6) *
                 (emission_probabilities[current_tag].get(words[i], 1e-6)),
                 prev_tag) for prev_tag in states)

            V[i][current_tag] = prob
            new_path[current_tag] = path[state] + [current_tag]

        path = new_path


    (max_prob, best_end_tag) = max((V[len(words)-1][tag], tag) for tag in states)
    return path[best_end_tag]


def read_sentences_from_file(file_path):
    sentences = []
    current_sentence = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                current_sentence.append(line)
            else:
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
        if current_sentence:
            sentences.append(current_sentence)

    return sentences


sentences = read_sentences_from_file(test_file_path)


for sentence in sentences:
    predicted_tags = viterbi_algorithm(sentence, transition_probabilities, emission_probabilities, tag_counts)

with open(output_file_path, "w") as out_file:
    for sentence in sentences:
        predicted_tags = viterbi_algorithm(sentence, transition_probabilities, emission_probabilities, tag_counts)
        for word, tag in zip(sentence, predicted_tags):
            out_file.write(f"{word}\t{tag}\n")
        out_file.write("\n")
