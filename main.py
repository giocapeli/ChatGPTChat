import key
import time
import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = key.OPENAI_API_KEY
app = Flask(__name__)

opener = ['Start a conversation or keep up with the subject.']
history_lines = []
history_lines_objects = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        new_opener = opener.copy()
        topic = request.form["topic"]
        if len(topic) > 0:
            new_opener.append(f'The topic is {topic}. ')
        else:
            new_opener.append("There is no main topic. ")
        str_opener = ' '.join(new_opener)
        for n in range(2):
            new_line(str_opener, "1")
            new_line(str_opener, "2")
        
        print(history_lines_objects)
    result = []
    for obj in history_lines_objects:
        result.append(f'{obj["person"]}: {obj["line"]}')
    return render_template("index.html", result=result)

def new_line(start_prompt, person):
    new_prompt = start_prompt
    new_prompt += f'You are the Person {person}.\n' 
    if len(history_lines_objects) > 0:
        for obj in history_lines_objects:
            new_prompt += f'Person {obj["person"]}: {obj["line"]}\n'
    new_prompt += f'Person {person}:'
    print('New prompt:\n'+ new_prompt)
    response = openai.Completion.create(
                model="text-davinci-003",
                prompt=new_prompt,
                temperature=0.6,
                max_tokens=1000
            )
    result = response.choices[0].text
    print('result:\n'+result)
    
    time.sleep(1)
    history_lines.append(f'Person {person}: {result}')
    history_lines_objects.append({
        "person": person,
        "line": result.strip()
    })

if __name__ == '__main__':
    app.run(debug=True)
    
