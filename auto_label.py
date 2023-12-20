import pickle

import requests
import json


def query_gpt3_label(question, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional comment dataset tagger and can find the most suitable label for each \
                comment. Now I will give you some comments about restaurant, you will give them a label represent their \
                topic, there are eight topics, food, hygiene, atmosphere, service, location, parking, transportation \
                and none. So no matter what I tell you, just answer one of these eight words"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
api_key = ""  # API key
DATA_FILE="data/raw_allsentense.json"
OUTPUT_FILE="data/labeled_sentense4.json"
labeleddata=[]
with open(DATA_FILE, "rb") as data:
    allsentense = json.load(data)
    for sentense in allsentense[10000:20000]:
        result = query_gpt3_label(sentense, api_key)
        print(result)
        labeleddata.append((sentense,result))

with open(OUTPUT_FILE,"w") as data:
    json.dump(labeleddata,data)



