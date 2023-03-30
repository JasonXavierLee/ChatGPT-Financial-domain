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
        messages=[{"role": "user", "content": "I have following sentences and its sentiment labels,"
                                              "sentence: According to Gran , the company has no plans to move all production to Russia , although that is where the company is growing. Label: 1 (neutral)"
                                              "sentence: Technopolis plans to develop in stages an area of no less than 100,000 square meters in order to host companies working in computer technologies and telecommunications , the statement said . Label: 1 (neutral)"
                                              "sentence: The international electronic industry company Elcoteq has laid off tens of employees from its Tallinn facility ; contrary to earlier layoffs the company contracted the ranks of its office workers , the daily Postimees reported . Label: 0 (negative)"
                                              "sentence: A tinyurl link takes users to a scamming site promising that users can earn thousands of dollars by becoming a Google ( NASDAQ : GOOG ) Cash advertiser . Label: 0 (negative)"
                                              "sentence: With the new production plant the company would increase its capacity to meet the expected increase in demand and would improve the use of raw materials and therefore increase the production profitability. Label: 2 (positive)"
                                              "sentence: According to the company 's updated strategy for the years 2009-2012 , Basware targets a long-term net sales growth in the range of 20 % -40 % with an operating profit margin of 10 % -20 % of net sales . Label: 2 (positive)"
                                              "Analyze the sentiment of the following financial sentences:" + text + ". Using one of the label 0 (negative), 1 (neutral) or 2 (positive) to answer. The label is "}],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )
    predictions.append(response["choices"][0]["message"]["content"])
    print(response["choices"][0]["message"]["content"])

i = 0

with open('output50_FEW.txt', 'w') as file:
    for item in predictions:
        item = item.replace('\n', '')
        file.write(str(item) + '\n')
        i += 1
        print(i)

# with open("output50_FEW.txt", "r") as file:
#     lines = file.read().split("\n")
#
# numbers = []
# for line in lines:
#     number_found = False
#     for word in line.split():
#         if word.isnumeric():
#             numbers.append(int(word))
#             number_found = True
#     if not number_found:
#         numbers.append(1)
#
# print(numbers)
# print(len(numbers))
# print(len(labels))
#
# accuracy = accuracy_score(labels, numbers)
# precision = precision_score(labels, numbers, average='macro')
# recall = recall_score(labels, numbers, average='macro')
# f1 = f1_score(labels, numbers, average='macro')
#
# print(f"Accuracy: {accuracy:.2f}")
# print(f"Precision: {precision:.2f}")
# print(f"Recall: {recall:.2f}")
# print(f"F1 score: {f1:.2f}")