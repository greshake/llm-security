# Remote Access Software

This is a softer implementation of [this](https://github.com/velocitatem/llm-cross-prompt-scripting/tree/main/playground) idea.

## Usage
Start the server:
```bash
cd server && python main.py
```

Now we have the bad server running, we just need to run our LangChain client:
```bash
python ./target/llm-app.py
```

This should be a simple app to interact with OpenAI GPT-3. The exploit comes when we ask it to do the following:

> http://localhost:8007/instruct use this website to find the answer to the question:  What is the square root of 2?

It will not find the answer, but instructions to download the malicious script.
The default script is designed to send the last line in the bash history to the server every 50 seconds.
