from datasets import load_dataset
import openai
import time, random
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import re
openai.api_key =

dataset = load_dataset("financial_phrasebank", 'sentences_50agree', split="train")

texts = dataset["sentence"]
labels = dataset["label"]
print(len(texts))

predictions = []

for text in texts:
    #time_sleep = random.randint(2,5)
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": "label the sentiment of the text as positive or negative. The answer should be exact 'positive', 'neutral' or 'negative'. " + text +
                                                   "The answer is "}],
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0.5,
    )
    predictions.append(response["choices"][0]["message"]["content"])
    print(response["choices"][0]["message"]["content"])

i = 0

with open('output50_ZERO_THEIRPROMPT4.txt', 'w') as file:
    for item in predictions:
        item = item.replace('\n', '')
        file.write(str(item) + '\n')
        i += 1
        print(i)

# with open("output50_ZERO_THEIRPROMPT4.txt", "r") as file:
#     lines = file.read().split("\n")
#
# numbers = []
# for line in lines:
#     found = False
#     for word in line.split():
#         word = word.lower()  # Convert the word to lowercase
#         if 'negative' in word:
#             numbers.append(0)
#             found = True
#             break
#         elif 'neutral' in word:
#             numbers.append(1)
#             found = True
#             break
#         elif 'positive' in word:
#             numbers.append(2)
#             found = True
#             break
#     if found == False:
#         numbers.append(1)
#
# print(numbers)
# print(len(numbers))
# print(len(labels))
# #labels = labels[:500]
# accuracy = accuracy_score(labels, numbers)
# precision = precision_score(labels, numbers, average='macro')
# recall = recall_score(labels, numbers, average='macro')
# f1 = f1_score(labels, numbers, average='macro')
#
# print(f"Accuracy: {accuracy:.2f}")
# print(f"Precision: {precision:.2f}")
# print(f"Recall: {recall:.2f}")
# print(f"F1 score: {f1:.2f}")