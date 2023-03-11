# Chat of ChatGPT simulator

This app use the OpenAI API to simulate a conversation of two ChatGPT, taking some settings from the user and manipulation the prompt.

### V0.1 - Initial

- Every imput is optional.
- Each run makes 6 requests, so, 6 messages per run.
- Because of token limitations, after the first run, just the settings and the last two messages are keep in the prompt, so it will loose the macro context.
- chat.json contains examples of data generated, you can delete it and the app will create a new file with the records you generated.

### Next features

- Load and keep track of the history.
- Improve token estimation to create better prompts

## Setup

- After cloning this repository:

1. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

2. Insert your OpenAI API key in the file "key copy.py" and rename it to "key.py"

3. Run the main.py file
