import json
import torch
import torch.nn as nn
from konlpy.tag import Okt
import random
import pandas as pd


class Net(nn.Module):
    def __init__(self, input_size, label_size):
        super(Net, self).__init__()

        self.layer = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, label_size)
        )

    def forward(self, x):
        return self.layer(x)


data = pd.read_json("./intents.json")
okt = Okt()

model = Net(37, 5)
model.load_state_dict(torch.load("./model.pt"))
model.eval()

max_length = 37
labels = ['greeting', 'question_1', 'question_2', 'question_3', 'bye']
with open("./data.json", "rt", encoding='utf-8') as f:
    words = json.load(f)


def inference(word):
    word = okt.morphs(word)

    one_hot_encoding = torch.zeros(max_length)

    if word in words:
        t_index = words.index(word)
        one_hot_encoding[t_index] = 1

    encoded_label = torch.argmax(model(one_hot_encoding))

    tag = labels[encoded_label]

    responses = list(filter(lambda x: x["tag"] == tag, data.intents.tolist()))
    response = random.choice(responses[0]["responses"])
    return response


if __name__ == "__main__":
    while True:
        user_input = input("You > ")
        print(inference(user_input))
