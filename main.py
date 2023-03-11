import key
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

testarray = [
  {
    "sender": "Alice",
    "text": "Hey, how are you?",
    "timestamp": "2022-03-10T13:45:00.000Z",
    "mine":True
  },
  {
    "sender": "Bob",
    "text": "I'm good, thanks for asking. How about you?",
    "timestamp": "2022-03-10T13:46:30.000Z"
  },
  {
    "sender": "Alice",
    "text": "I'm doing well too, thanks.",
    "timestamp": "2022-03-10T13:48:15.000Z",
    "mine":True
  },
  {
    "sender": "Bob",
    "text": "That's great to hear!",
    "timestamp": "2022-03-10T13:49:00.000Z"
  }
]

openai.api_key = key.OPENAI_API_KEY
app = Flask(__name__)

opener = ['Start a conversation or keep up with the subject.']
history_lines = []
history_lines_objects = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        new_opener = opener.copy()
        topic = request.form.get("topic", "")
        if topic:
            new_opener.append(f"The topic is {topic}. ")
        else:
            new_opener.append("There is no main topic. ")
        str_opener = " ".join(new_opener)
        for _ in range(2):
            new_line(str_opener, "1")
            new_line(str_opener, "2")
        print(history_lines_objects)
    result = [f"{obj['sender']}: {obj['text']}" for obj in history_lines_objects]
    return render_template("index.html", messages=testarray)

def new_line(start_prompt, person):
    new_prompt = f"{start_prompt}You are the Person {person}.\n"
    if history_lines_objects:
        new_prompt += "".join(f"Person {obj['sender']}: {obj['text']}\n" for obj in history_lines_objects)
    else:
        new_prompt += "Person 2: Hello, you!\n"
    new_prompt += f"Person {person}:"
    # print(f"New prompt:\n{new_prompt}")
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=new_prompt,
    #     temperature=0.6,
    #     max_tokens=1000,
    # )
    # result = response.choices[0].text
    result = "test"
    print(f"Result:\n{result}")
    time.sleep(1)
    line = f"Person {person}: {result.strip()}"
    history_lines.append(line)
    history_lines_objects.append({"sender": person, "text": result.strip()})

if __name__ == "__main__":
    app.run(debug=True)
