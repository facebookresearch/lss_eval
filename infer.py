# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

def load_model(model_path):
    model = AutoModelWithLMHead.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer

def generate_text(model, tokenizer, reference, claim):
    combined_input = f"Reference: {reference}\nClaim: {claim}\nOutput:"
    return pipeline('text-generation', model=model, tokenizer=tokenizer)(combined_input)

def main():
    model_path = "/path/to/your/model"  # replace this with your model path
    reference = input("Please enter the reference: ")
    claim = input("Please enter the claim: ")
    model, tokenizer = load_model(model_path)
    output = generate_text(model, tokenizer, reference, claim)
    print(output)

if __name__ == "__main__":
    main()
