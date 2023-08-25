# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

def load_model(model_path):
    model = AutoModelWithLMHead.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer

def generate_text(model, tokenizer, reference, claim):
    combined_input = f"Reference: {reference}\nClaim: {claim}\nOutput:"
    result = pipeline('text-generation', model=model, tokenizer=tokenizer)(combined_input)
    return result[0]['generated_text'].split('Output: ')[-1].strip()

def calculate_bleu(reference, hypothesis):
    smoothie = SmoothingFunction().method4
    return sentence_bleu([reference.split()], hypothesis.split(), smoothing_function=smoothie)

def main():
    model_path = "/path/to/your/model"  # replace this with your model path
    model, tokenizer = load_model(model_path)

    # Read CSV file
    df = pd.read_csv('path/to/your/file')

    # Generate output for each reference-claim pair
    df['LSS'] = df.apply(lambda row: generate_text(model, tokenizer, row['Reference'], row['Claim']), axis=1)

    # Calculate BLEU score for each row and save in new column
    df['LSS_BLEU'] = df.apply(lambda row: calculate_bleu(row['Claim'], row['LSS']), axis=1)

    # Save to new CSV
    df.to_csv('output.csv', index=False)

    # Calculate and print the average BLEU score
    avg_bleu = df['LSS_BLEU'].mean()
    print(f"Faithfulness Score: {avg_bleu}")

if __name__ == "__main__":
    main()
