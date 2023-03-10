import key
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = key.OPENAI_API_KEY
app = Flask(__name__)

opener = ['Pretend your talking to a friend so answer his question or make a new question following the conversation.']
history_lines = []
history_lines_objects = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        new_opener = opener.copy()
        topic = request.form["topic"]
        if len(topic) > 0:
            new_opener.append(f'The starting topic is: {topic}. ')
        else:
            new_opener.append("Start with any topic. ")
        str_opener = ' '.join(new_opener)
        new_line(str_opener, "you")
        new_line(str_opener, "friend")
        new_line(str_opener, "you")
        new_line(str_opener, "friend")
        new_line(str_opener, "you")
        
        print(history_lines_objects)
    result = ''
    for obj in history_lines_objects:
        result += f'{obj["person"]}: {obj["line"]}\n'
    return render_template("index.html", result=result)

def new_line(prompt, person):
    for obj in history_lines_objects:
        if obj['person'] == person:
            person_line = 'You'
        else:
            person_line = 'Friend'
        prompt += f'{person_line}: {obj["line"]}\n'
    prompt += f'You:'

    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.6,
                max_tokens=1000
            )
    result = response.choices[0].text
    time.sleep(3)
    history_lines.append(f'Person {person}: {result}')
    history_lines_objects.append({
        "person": person,
        "line": result.strip()
    })

if __name__ == '__main__':
    app.run(debug=True)
    
