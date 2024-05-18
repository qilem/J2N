import torch
from transformers import BertTokenizer, BertForTokenClassification
from torch.utils.data import Dataset
import os
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK sentence tokenizer data if not already present
nltk.download('punkt')

# Define the dataset class for loading data
class NominalAdjectiveDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoded = self.tokenizer(self.texts[idx], is_split_into_words=True, truncation=True, padding='max_length', max_length=self.max_length)
        input_ids = encoded['input_ids']
        attention_mask = encoded['attention_mask']

        return {'input_ids': torch.tensor(input_ids, dtype=torch.long),
                'attention_mask': torch.tensor(attention_mask, dtype=torch.long)}

# Function to load the trained model and tokenizer
def load_model_and_tokenizer(model_path):
    model = BertForTokenClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    return model, tokenizer

# Function to make predictions
def predict_nominal_adjectives(texts, model, tokenizer, max_length=128):
    dataset = NominalAdjectiveDataset(texts, tokenizer, max_length=max_length)
    loader = torch.utils.data.DataLoader(dataset, batch_size=1)

    model.eval()
    predictions = []

    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(model.device)
            attention_mask = batch['attention_mask'].to(model.device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1).cpu().numpy()

            for i, input_id in enumerate(input_ids):
                tokens = tokenizer.convert_ids_to_tokens(input_id)
                pred_labels = preds[i]
                predictions.append((tokens, pred_labels))

    return predictions

# Function to process predictions and get the words after nominal adjectives
def retrieve(predictions, label_map):
    ans = []
    for tokens, labels in predictions:
        sentence_words = []
        for i, (token, label) in enumerate(zip(tokens, labels)):
            if label_map.get(label) == 'nominal_adjective':
                for follow_token in tokens[i+1:]:
                    if follow_token and follow_token not in ['[CLS]', '[SEP]', '[PAD]', '.', ',', ';', '!', '?']:
                        sentence_words.append(follow_token)
                        break
        ans.append(sentence_words)
    return ans

# Define label map (adjust based on your label IDs)
label_map = {0: 'O', 1: 'nominal_adjective'}

# Main function to run the prediction pipeline
def main():
    model_path = './bert_nominal_adjective'  # Fixed model path
    model, tokenizer = load_model_and_tokenizer(model_path)
    model.to('cuda' if torch.cuda.is_available() else 'cpu')

    while True:
        user_input = input("Enter a single sentence or a file path (type 'stop' to end): ")

        if user_input.lower() == 'stop':
            break

        if os.path.isfile(user_input):
            with open(user_input, 'r') as file:
                text = file.read()
            sentences = sent_tokenize(text)
            predictions = predict_nominal_adjectives(sentences, model, tokenizer, max_length=128)
            ans = retrieve(predictions, label_map)
            output_file = 'output_predictions.txt'
            with open(output_file, 'w') as out_file:
                for sentence, words in zip(sentences, ans):
                    out_file.write(f"Text: {sentence.strip()}\n")
                    if len(words) == 0:
                        out_file.write('There is no nominal adjective.\n')
                    else:
                        out_file.write(f"nominal adjectives: {', '.join(words)}\n\n")

            print(f"Results will be written to {output_file}")
        else:
            texts = [user_input]
            predictions = predict_nominal_adjectives(texts, model, tokenizer, max_length=128)
            ans = retrieve(predictions, label_map)
            if len(ans) == 0 or len(ans[0]) == 0:
                print('There is no nominal adjective.')
            else:
                for text, words in zip(texts, ans):
                    print(f"nominal adjectives: {', '.join(words)}")

if __name__ == "__main__":
    main()
