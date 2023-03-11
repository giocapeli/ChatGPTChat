import key
import time
import openai
import json
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = key.OPENAI_API_KEY
app = Flask(__name__)

person_a_name = "Bruce"
person_b_name = "Kate"
type_of_conversation = "casual"
history_lines_objects = []

@app.route("/", methods=("GET", "POST"))
def index():
    conversation_id = time.strftime("%H%M%S", time.localtime())
    if request.method == "POST":
        topic = request.form.get("topic", "")
        type_of_conversation = request.form.get("type", "")
        new_opener = [f'Start a {type_of_conversation} conversation or keep up with the subject.']
        print(new_opener)
        kate_mood = request.form.get("kate_mood", "")
        bruce_mood = request.form.get("bruce_mood", "")
        settings = {
            "topic":topic,
            "type":type_of_conversation,
            "kate_mood":kate_mood,
            "bruce_mood":bruce_mood
        }
        person_a = {
            "name": person_a_name,
            "mood": kate_mood
        }
        person_b = {
            "name": person_b_name,
            "mood": bruce_mood
        }
        str_opener = " ".join(new_opener)
        for _ in range(3):
            new_line(str_opener, person_a, settings, person_b)
            new_line(str_opener, person_b, settings, person_a)
        save_chat(settings, history_lines_objects, conversation_id)
    return render_template("index.html", messages=history_lines_objects)

def new_line(start_prompt, person, settings, other_person):
    new_prompt = f"{start_prompt} You are {person['name']} and you're talking to {other_person['name']}, you mood is {person['mood']} but don't say it directly.\n"
    new_history_lines_objects = history_lines_objects.copy()
    if new_history_lines_objects:
        if len(new_history_lines_objects) > 2:
            new_history_lines_objects = new_history_lines_objects[len(new_history_lines_objects)-2:]
        new_prompt += "".join(f"{obj['sender']}: {obj['text']}\n" for obj in new_history_lines_objects)
    else:
        new_prompt += f"{person_b_name}: Hello, you! "
        if len(settings["topic"]):
            new_prompt += f'What do you think about {settings["topic"]}?'
    new_prompt += f"\n{person['name']}:"
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
    line = f"{person['name']}: {result.strip()}"
    history_lines_objects.append({"sender": person['name'], "text": result.strip(),"time": time.strftime("%H:%M:%S", time.localtime()), "mine":person['name'] == person_a_name})

def save_chat(settings, lines, conversation_id):
    history = {
        conversation_id:{
            time.strftime("%H:%M:%S", time.localtime()):{
                "settings":settings,
                "lines":lines
            }
        }
    }
    loaded_data = history
    try:
        with open("chat.json", "r") as data_file:
            loaded_data = json.load(data_file)
            loaded_data.update(history)
            data_file.close()
    except FileNotFoundError:
        pass
    finally:
        with open("chat.json", "w") as data_file:
            json.dump(loaded_data, data_file, indent=4)
            data_file.close()

if __name__ == "__main__":
    app.run(debug=True)
