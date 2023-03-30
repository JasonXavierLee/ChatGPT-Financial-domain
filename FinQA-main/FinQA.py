import openai
import json

openai.api_key =

with open('C:/important/queens/lab/Fact/ChatGPT/Dataset/FinQA/FinQA-main/dataset/test.json', 'r') as file:
    data = json.load(file)

print(data[0].keys())

selected_keys = ['pre_text', 'table', 'post_text', 'qa']
new_data = [{key: element[key] for key in selected_keys} for element in data]
print(len(new_data))

for element in new_data:
    if isinstance(element['pre_text'], list):
        element['pre_text'] = ' '.join(element['pre_text'])
    element['pre_text'] += " The following is a table: "

    if isinstance(element['post_text'], list):
        element['post_text'] = ' '.join(element['post_text'])
    element['post_text'] = "That's the end of the table. \n" + element['post_text']

def table_to_string(table):
    # Assuming the table is a list of lists
    table_string = ""
    for row in table:
        row_string = ', '.join([str(item) for item in row])
        table_string += row_string + '\n'
    return table_string

combined = []
for element in new_data:
    # Convert table to string, if needed
    table_string = table_to_string(element['table'])

    # Combine 'pre_text', 'table', and 'post_text'
    combined.append(element['pre_text'] + '\n' + table_string + '\n' + element['post_text'] + '\n' + element['qa']['question'])

print(combined[0])

labels = [element['qa']['answer'] for element in data]
# print(labels[0])
# with open('labels.txt', 'w') as file:
#     for item in labels:
#         file.write(item + '\n')


history = []

for text in combined:
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[{"role": "user", "content": text + " put the brief answer in the curly bracket, the answer is"}],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    history.append(response["choices"][0]["message"]["content"])
    print(response["choices"][0]["message"]["content"])

i = 0
with open('labels_GPT4.txt', 'w') as file:
    for item in history:
        item = item.replace('\n', '')
        file.write(str(item) + '\n')
        i += 1
        print(i)