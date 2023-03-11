import key
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = key.OPENAI_API_KEY
app = Flask(__name__)

person_a = "Bruce"
person_b = "Kate"
type_of_conversation = "casual"

opener = [f'Start a {type_of_conversation} conversation or keep up with the subject.']
history_lines = []
history_lines_objects = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        new_opener = opener.copy()
        topic = request.form.get("topic", "")
        type_of_conversation = request.form.get("type", "")
        str_opener = " ".join(new_opener)
        for _ in range(3):
            new_line(str_opener, person_a, topic)
            new_line(str_opener, person_b, topic)
        print(history_lines_objects)
    return render_template("index.html", messages=history_lines_objects)

def new_line(start_prompt, person, topic):
    new_prompt = f"{start_prompt}You are {person}.\n"
    if history_lines_objects:
        new_prompt += "".join(f"{obj['sender']}: {obj['text']}\n" for obj in history_lines_objects)
    else:
        new_prompt += f"{person_b}: Hello, you! "
        if len(topic):
            new_prompt += f'What do you think about {topic}?'
    new_prompt += f"\n{person}:"
    print(f"New prompt:\n{new_prompt}")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_prompt,
        temperature=0.6,
        max_tokens=1000,
    )
    result = response.choices[0].text
    print(f"Result:\n{result}")
    time.sleep(1)
    line = f"{person}: {result.strip()}"
    history_lines.append(line)
    history_lines_objects.append({"sender": person, "text": result.strip(),"time": time.strftime("%H:%M:%S", time.localtime()), "mine":person == person_a})

if __name__ == "__main__":
    app.run(debug=True)
