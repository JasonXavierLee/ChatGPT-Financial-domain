from datasets import load_dataset
import openai
from torch.utils.data import DataLoader
import time, random
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import re
openai.api_key =

### Change here to True if rate limit error!!!!!!!!!!!!!!!!!!!!!!!!
# if not suggest no batch data, I find different responses if batched
batch_data = False


# Load the dataset
dataset = load_dataset("glue", "sst2", split='validation')
labels = dataset["label"]
print(dataset['sentence'])

if batch_data == True:
    # Define the prompt
    prompt = "For each of above 20 texts, label the sentiment of the text as positive or negative. The answer should be exact 'positive' or 'negative'."

    # Convert the dataset into a list of dictionaries
    dataset_list = [{"sentence": item['sentence'], "label": item['label']} for item in dataset]

    # Extract the labels from the dataset_list
    labels = [item['label'] for item in dataset_list]

    # Group the data into batches of 20
    # 5, 10 ,20 ,50 ,100
    batch_size = 20
    batches = [dataset_list[i:i + batch_size] for i in range(0, len(dataset_list), batch_size)]


    # Function to send a list of messages to the API
    def chat(messages, model="gpt-3.5-turbo"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["message"]["content"].strip()

    responses = []

    for batch in batches:
        print(len(batch))
        messages = []
        for item in batch:
            sentence = item['sentence']
            messages.append({"role": "user", "content": sentence})
        messages.append({"role": "user", "content": prompt})
        print(messages)
        # Call the API
        result = chat(messages)

        # Split the response into individual answers
        answers = result.split("\n")
        print(answers)
        responses.append(answers)

    # Flatten the list of responses
    responses = [answer for batch_responses in responses for answer in batch_responses]

    print(responses)

else:
    texts = dataset["sentence"]
    labels = dataset["label"]
    print(len(texts))

    responses = []

    for text in texts:
        # time_sleep = random.randint(2,5)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "label the sentiment of the text as positive or negative. The answer should be exact 'positive' or 'negative'. " + text +
                                                  "The answer is "}],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        responses.append(response["choices"][0]["message"]["content"])
        print(response["choices"][0]["message"]["content"])

i = 0

with open('output_SST2_DEV_1B1.txt', 'w') as file:
    for item in responses:
        item = item.replace('\n', '')
        file.write(str(item) + '\n')
        i += 1
        print(i)

# with open("output_SST2_DEV_1B1.txt", "r") as file:
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
#         elif 'positive' in word:
#             numbers.append(1)
#             found = True
#             break
#     if found == False:
#         numbers.append(0)
#
#
# print(numbers)
# print(labels)
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