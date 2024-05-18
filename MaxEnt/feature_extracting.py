import sys
import string

def is_punctual(word):

  if all(char in string.punctuation for char in word):
    return "FullPunct"
  elif word and any(char in string.punctuation for char in word):
    return "PartPunct"
  else:
    return "FullWord"


def capitalized(word):

    if word.isupper():
        return "AllCaps"
    elif word.istitle():
        return "InitCap"
    else:
        return "Lower"


def extract_features(input_file, output_file, is_training):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Initialize the variables with special values
        prev_word, prev_pos, prev_chunk = "STARTT", "STARTT", "STARTT"
        prev_prev_word, prev_prev_pos, prev_prev_chunk = "STARTT", "STARTT", "STARTT"
        prev_prev_prev_word, prev_prev_prev_pos, prev_prev_prev_chunk = "STARTT", "STARTT", "STARTT"

        lines = infile.readlines()  # Read all lines into a list

        for i, line in enumerate(lines):
            line = line.strip()

            # Handle blank lines
            if not line:
                outfile.write("\n")
                prev_word, prev_pos, prev_chunk = "STARTT", "STARTT", "STARTT"
                prev_prev_word, prev_prev_pos, prev_prev_chunk = "STARTT", "STARTT", "STARTT"
                prev_prev_prev_word, prev_prev_prev_pos, prev_prev_prev_chunk = "STARTT", "STARTT", "STARTT"

                continue

            parts = line.split("\t")  # Splitting by tab character

            if len(parts) >= 3:
                word, pos, chunk = parts[0], parts[1], parts[2]  # Extracting word, POS, and BIO tag
            else:
                word, pos, chunk = parts[0], parts[1], ''  # Skip lines with fewer than three columns

            # Get the next words, POS tags, and BIO tags using a window of size 3
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line:
                    next_parts = next_line.split("\t")
                    next_word, next_pos, next_chunk = next_parts[0], next_parts[1], next_parts[2] if len(next_parts) >= 3 else "ENDD"
                    next_is_capitalized = capitalized(next_word)
                    is_next_word_punctual = is_punctual(next_word)
                else:
                    next_word, next_pos, next_chunk = "ENDD", "ENDD", "ENDD"
                    next_is_capitalized="ENDD"
                    is_next_word_punctual ="ENDD"
            else:
                next_word, next_pos, next_chunk = "ENDD", "ENDD", "ENDD"
            flag=0
            if next_word=="ENDD":
                flag=1
            if i + 2 < len(lines) and flag==0:
                next_next_line = lines[i + 2].strip()
                if next_next_line:
                    next_next_parts = next_next_line.split("\t")
                    if len(next_next_parts) >= 3:
                        next_next_word, next_next_pos, next_next_chunk = next_next_parts[0], next_next_parts[1], next_next_parts[2]
                    elif len(next_next_parts) >= 2:
                        next_next_word, next_next_pos = next_next_parts[0], next_next_parts[1]
                    else:
                        next_next_word, next_next_pos, next_next_chunk = "ENDD", "ENDD", "ENDD"
                else:
                    next_next_word, next_next_pos, next_next_chunk = "ENDD", "ENDD", "ENDD"
            else:
                next_next_word, next_next_pos, next_next_chunk = "ENDD", "ENDD", "ENDD"
            if next_next_word=="ENDD":
                flag=1
            if i + 3 < len(lines) and flag==0:
                next_next_next_line = lines[i + 3].strip()
                if next_next_next_line:
                    next_next_next_parts = next_next_next_line.split("\t")
                    if len(next_next_next_parts) >= 3:
                        next_next_next_word, next_next_next_pos, next_next_next_chunk = next_next_next_parts[0], next_next_next_parts[1], \
                                                                         next_next_next_parts[2]
                    elif len(next_next_next_parts) >= 2:
                        next_next_next_word, next_next_next_pos = next_next_next_parts[0], next_next_next_parts[1]
                    else:
                        next_next_next_word, next_next_next_pos, next_next_next_chunk = "ENDD", "ENDD", "ENDD"
                else:
                    next_next_next_word, next_next_next_pos, next_next_next_chunk = "ENDD", "ENDD", "ENDD"
            else:
                next_next_next_word, next_next_next_pos, next_next_next_chunk = "ENDD", "ENDD", "ENDD"
            punct=is_punctual(word)
            is_capitalized=capitalized(word)
            if prev_word=="STARTT":
                prev_is_capitalized = "STARTT"
                is_prev_word_punctual = "STARTT"
            else:
                prev_is_capitalized = capitalized(prev_word)
                is_prev_word_punctual = is_punctual(prev_word)

            feature_line = f"{word}\t"
            feature_line += f"pos={pos}\t"
            feature_line += f"prev_word={prev_word}\t"
            feature_line += f"next_word={next_word}\t"
            feature_line += f"prev_POS={prev_pos}\t"
            feature_line += f"prev_prev_POS={prev_prev_pos}\t"
            feature_line += f"prev_prev_prev_POS={prev_prev_prev_pos}\t"
            feature_line += f"next_POS={next_pos}\t"
            feature_line += f"next_next_POS={next_next_pos}\t"
            feature_line += f"next_next_next_POS={next_next_next_pos}\t"
            feature_line += f"all_POS={prev_prev_prev_pos+prev_prev_pos+prev_pos+pos+next_pos+next_next_pos+next_next_next_pos}\t"
            feature_line += f"some_POS={prev_prev_pos+prev_pos+pos+next_pos+next_next_pos}\t"
            feature_line += f"two_prev_POS={prev_prev_pos + prev_pos + pos}\t"
            feature_line += f"three_prev_POS={prev_prev_prev_pos+prev_prev_pos+prev_pos+pos}\t"
            feature_line += f"two_next_POS={pos+next_pos+next_next_pos}\t"
            feature_line += f"three_next_POS={pos+next_pos+next_next_pos+next_next_next_pos}\t"
            feature_line += f"part_POS={prev_pos + pos + next_pos}\t"
            feature_line += f"front_POS={prev_pos + pos}\t"
            feature_line += f"back_POS={pos+next_pos}\t"
            feature_line += f"front_word={prev_word + word}\t"
            feature_line += f"back_word={word + next_word}\t"
            feature_line += f"is_capitalized={prev_is_capitalized+is_capitalized+next_is_capitalized}\t"
            feature_line += f"is_word_punctual={is_prev_word_punctual+punct+is_next_word_punctual}"

            if is_training:
                feature_line += "\t"
                feature_line += chunk

            outfile.write(feature_line + "\n")

            # Rotate the variables for the next line
            prev_prev_prev_word, prev_prev_prev_pos, prev_prev_prev_chunk = prev_prev_word, prev_prev_pos, prev_prev_chunk
            prev_prev_word, prev_prev_pos, prev_prev_chunk = prev_word, prev_pos, prev_chunk
            prev_word, prev_pos, prev_chunk = word, pos, chunk

# Unified feature extraction method call
if len(sys.argv) == 5:
    train_input_file, train_output_file, test_input_file, test_output_file = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    extract_features(train_input_file, train_output_file, is_training=True)
    extract_features(test_input_file, test_output_file, is_training=False)