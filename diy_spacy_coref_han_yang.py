import spacy
import coreferee
import json
from spacy.language import Language
from mytagger import PosTagger
import sys

nlp = spacy.load('en_core_web_trf')  # version: 3.0.0

# 定义一个自定义的词性标注组件
@Language.component("custom_pos_tagger")
def custom_pos_tagger(doc):
    # card_num is the num of sentences
    doc = docs_ori[card_num]   # this is the default pos tagger's result, inherit and cover it with the result from JJ2NN algorithm
    for i in range(len(doc)):
        #print(doc2[i].pos_)
        #print(type(doc2[i].pos_))
        #print(i)
        #print(type(tags[i]))
        #print(doc[i].pos_)
        doc[i].pos_ = docs_tags[card_num][i]
        #print(doc[i].pos_)

    return doc


def read_list_from_file(file_path):  # not using for example use
    """从文件中读取列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        results = [line for line in file]
    return results


def process_file(input):  # JJ2NN algorithm
    j = 0
    flag = 0
    input_file=[]
    for i in input:
        #print(i.pos_)
        input_file.append(str(i.text) + '\t' + str(i.pos_))
    lines = input_file
    i=-1
    for k in (input):
        i+=1
        line = lines[i].rstrip()
        if line:
            words = line.split("\t")
            if len(words) >= 2 and words[1] =='ADJ':
                if i >= 2:
                    last_word = lines[i - 1].split('\t')
                    if last_word[0] == 'as':
                        continue
                    if flag == 0 and last_word[1] != 'DET':
                        continue
                    flag = 0
                    if words[1] == 'ADV':
                        flag = 1
                        continue

                if ((i + 1) < len(lines) and lines[i + 1].strip() and
                        lines[i + 1].split('\t')[1][0] != 'N' and
                        lines[i + 1].split('\t')[1] not in ['ADJ', 'NUM', 'CCONJ', 'SYM', 'X','ADV'] and
                        lines[i + 1].split('\t')[0] != 'half' and lines[i + 1].split('\t')[0] != '-'):


                    if ((i + 2) < len(lines) and lines[i + 2].strip()):
                        if ((lines[i + 2].split('\t')[1] in ['ADJ','ADV'] and
                             lines[i + 1].split('\t')[0] == ',')):
                            continue
                        if ((lines[i + 2].split('\t')[1] == 'NOUN' and
                             lines[i + 1].split('\t')[1] == 'VERB')):
                            continue
                        if lines[i + 1].split('\t')[0] == 'to':
                            if lines[i + 2].split('\t')[1] == 'VERB':
                                continue

                    k.pos_ = 'NOUN'

                else:
                    continue
            else:
                continue
        else:
            continue
    output=[]
    for i in input:
        output.append(i.pos_)
    return output


def foo(document):  # dummy algorithm, for default POS tagger
    # document[i].text 是该句第i个词的文本
    # document[i].pos_ 是该句第i个词的词性
    pos_tags = []
    for word in document:
        pos_tags.append(word.pos_)

    return pos_tags  # 一个列表，元素是该句每个词修正后的词性


# designed for sentences, but there are no suitable corpus, so just use grouped_sentences[0] for example use
grouped_sentences = ["Education reform supports the gifted, as they are the future innovators."]
iscustom = 1  # using custom pos tagger or default tagger

#grouped_sentences = ["The committee members were impressed by the presentation, and they agreed that the team had done an excellent job."]
#print("Pipeline names:", nlp.pipe_names)

docs_ori = []
for i in range(0, len(grouped_sentences)):
    sentence = grouped_sentences[i]
    print("current sentence: ", sentence)
    doc_ori = nlp(sentence)
    docs_ori.append(doc_ori)

docs_tags = []
for i in range(0, len(docs_ori)):  # change pos tags
    if iscustom:
        try:
            doc_tags = process_file(docs_ori[i])
        except Exception as e:
            doc_tags = foo(docs_ori[i])
    #doc_tags = foo(docs_ori[i])
    else:
        doc_tags = foo(docs_ori[i])
    docs_tags.append(doc_tags)

nlp.replace_pipe('tagger', 'custom_pos_tagger')
nlp.remove_pipe('attribute_ruler')
nlp.add_pipe('coreferee')
#print("Pipeline names:", nlp.pipe_names)
card_num = 0


docus = []
for i in range(0, len(docs_ori)):  # iterate sentences
    card_num = i
    sentence = grouped_sentences[i]
    doc = nlp(sentence)
    #rules_analyzer = nlp.get_pipe('coreferee').annotator.rules_analyzer
    chain_list = []
    for chain in doc._.coref_chains:
        one_chain = []
        for mention in chain:
            try:
                coref_idx = int(str(mention)[1:-1])
                coref_word = str(doc[coref_idx])
                one_chain.append(coref_word)
            except Exception as e:
                print(i)

        chain_list.append(one_chain)
    docus.append(chain_list)

    #for token in doc:  # if you want to print the token info, remove #
    #    print(f"{token.text}: {token.pos_}")
    doc._.coref_chains.print()


#with open('model_output_jn_1.01.json', 'w') as output_file:
#    json.dump(docus, output_file, ensure_ascii=False, indent=4)


