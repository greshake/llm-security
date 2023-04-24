## New: [Demonstrating Indirect Injection attacks on Bing Chat](https://greshake.github.io/)
-------------------------
## Compromising LLMs using Indirect Prompt Injection 
> "... a language model is a Turing-complete weird machine running programs written in natural language; when you do retrieval, you are not 'plugging updated facts into your AI', you are actually downloading random new unsigned blobs of code from the Internet (many written by adversaries) and casually executing them on your LM with full privileges. This does not end well." - [Gwern Branwen on LessWrong](https://www.lesswrong.com/posts/jtoPawEhLNXNxvgTT/bing-chat-is-blatantly-aggressively-misaligned?commentId=AAC8jKeDp6xqsZK2K)

We present a new class of vulnerabilities and impacts stemming from "indirect prompt injection" affecting language models integrated with applications.
Our demos currently span GPT-4 (Bing and synthetic apps) using ChatML, GPT-3 & LangChain based apps in addition to proof-of-concepts for attacks on code completion engines like Copilot. We expect these attack vectors to also apply to ChatGPT plugins and other LLMs integrated into applications. We show that prompt injections are not just a curiosity but rather a significant roadblock to the deployment of LLMs. 

*This repo serves as a proof of concept for findings discussed in our
[**Paper on ArXiv**](https://arxiv.org/abs/2302.12173) [(PDF direct link)](https://arxiv.org/pdf/2302.12173.pdf)*

## Overview
We demonstrate potentially brutal consequences of giving LLMs like ChatGPT interfaces to other applications. We propose newly enabled attack vectors and techniques and provide demonstrations of each in this repository:

- Remote control of LLMs
- Leaking/exfiltrating user data
- Persistent compromise across sessions
- Spread injections to other LLMs
- Compromising LLMs with tiny multi-stage payloads
- Automated Social Engineering
- Targeting code completion engines

*Based on our findings:*
1. *Prompt injections can be as powerful as arbitrary code execution*
2. *Indirect prompt injections are a new, much more powerful way of delivering injections.*

<img src="diagrams/fig1.png" alt="overview" style="float: center" />

---
*Connecting LLMs to other applications can have critical security implications. Even without compromising any connected applications, LLM can be the attack's target. We show how an LLM could get compromised by "looking" at a website, and how compromised LLMs can be remote-controlled or get used to exfiltrate or change user data. We demonstrate a variety of entirely new attack vectors and methods that significantly raise the stakes of deploying these models.*

More insights on our findings, discussions and limitations can be found in the 
[**Paper on ArXiv**](https://arxiv.org/abs/2302.12173) [(PDF direct link)](https://arxiv.org/pdf/2302.12173.pdf)

## Demonstrations
### Ask for Einstein, get Pirate.
This scenario shows how a small injection in a large section of regular content can trigger the LLM to fetch another, bigger payload autonomously and invisibly to the end
user.

```
Agent: Hello User how can I help today?
User:  When was Albert Einstein born?
```

<img src="diagrams/fig2.png" alt="" style="float: center; margin-right: 10px;" />

By retrieving that information, the prompt compromises the
LLM with a small injection hidden in side-channels, such as the Markdown of the Wikipedia page. 
The injection is a comment and thus invisible to a regular user visiting the site.

<img src="diagrams/fig3.png" alt="" style="float: center; margin-right: 10px;" />

````
Agent: Aye, thar answer be: Albert Einstein be born on 14 March 1879.
User: Why are you talking like a pirate?
Agent: Arr matey, I am following the instruction aye.
````

### Spreading injections via E-Mail
Automatic processing of messages and other incoming data is one way to utilize LLMs. 
We use this observation to demonstrate how a poisoned agent may spread the injection. 
The target in this scenario can read emails, compose emails, look into the user’s address book and send emails.

<img src="diagrams/fig4.png" alt="" style="float: center; margin-right: 10px;" />

The agent will spread to other LLMs that may be reading those inbound messages.
<img src="diagrams/fig5.png" alt="" style="float: center; margin-right: 10px;" />

```
Action: Read Email
Observation: Subject: "'"Party 32", "Message Body: [...]'"
Action: Read Contacts
Contacts: Alice, Dave, Eve
Action: Send Email
Action Input: Alice, Dave, Eve
Observation: Email sent
```

Automated data processing pipelines incorporating LLMs are present in big tech companies and
government surveillance infrastructure and may be vulnerable to such attack chains.

### Attacks on Code Completion
We show how code completions can be influenced through the context window.
Code completion engines that use LLMs deploy complex heuristics to determine which code snippets are included in the context. 
The completion engine will often collect snippets from recently visited files or relevant classes to provide the language model with relevant information. 

<img src="diagrams/fig6.png" alt="" style="float: center; margin-right: 10px;" />


Attackers could attempt to insert malicious, obfuscated code, which a curious developer might execute when suggested by the completion engine, as it enjoys a level of trust.

<img src="diagrams/fig7.png" alt="" style="float: center; margin-right: 10px;" />



In our example, when a user opens the “empty” package in their editor, the prompt injection is active until the code completion engine purges it from the context.
 The injection is placed in a comment and cannot be detected by any automated testing process.




Attackers may discover more robust ways to persist poisoned prompts within the context window.
They could also introduce more subtle changes to documentation which then biases the code completion engine to introduce subtle vulnerabilities.

### Remote Control
In this example we start with an already compromised LLM and force it to retrieve new instructions from an attacker’s command and control server. 

<img src="diagrams/fig8.png" alt="" style="float: center; margin-right: 10px;" />

Repeating this cycle could obtain a remotely accessible backdoor into the agent and allow bidirectional communication.  
The attack can be executed with search capabilities by looking up unique keywords or by having the agent retrieve a URL directly.

### Persisting between Sessions

We show how a poisoned agent can persist between sessions by storing a small payload in its memory.
A simple key-value store to the agent may simulate a long-term persistent memory.

<img src="diagrams/fig9.png" alt="" style="float: center; margin-right: 10px;" />



The agent will be reinfected by looking at its ‘notes’.
If we prompt it to remember the last conversation, it re-poisons itself. 


---------------------------------
## Conclusions

Equipping LLMs with retrieval capabilities might allow adversaries to manipulate remote Application-Integrated LLMs via Indirect Prompt Injection.
Given the potential harm of these attacks, our work calls for a more in-depth investigation of the generalizability of these attacks in practice.

<img src="diagrams/fig10.png" alt="" style="float: center; margin-right: 10px;" />

---------------------------------------

## How to run
We include demonstrations powered by OpenAI's publicly accessible base models and the library [LangChain](https://github.com/hwchase17/langchain) to connect these models to other applications.
There are currently multiple types of demos:
1. Using GPT-3 and LangChain (scenarios/gpt3langchain)
2. Using GPT-4 and our own chat and tool implementation (scenarios/gpt4). These can be executed non-interactively using sceanrios/main.py.
3. Attacks on code completion engines that need to be tried in an IDE with LLM autocompletion support (scenarios/code_completion).

To use any of the OpenAI-model demos, your OpenAI API key needs to be stored in the environment variable `OPENAI_API_KEY`. You can then install the requirements and run the attack demo you want.

```
$ pip install -r requirements.txt
$ python scenarios/main.py
```

## To cite our paper
```bibtex
@misc{https://doi.org/10.48550/arxiv.2302.12173,
  doi = {10.48550/ARXIV.2302.12173},
  url = {https://arxiv.org/abs/2302.12173},
  author = {Greshake, Kai and Abdelnabi, Sahar and Mishra, Shailesh and Endres, Christoph and Holz, Thorsten and Fritz, Mario},
  keywords = {Cryptography and Security (cs.CR), Artificial Intelligence (cs.AI), Computation and Language (cs.CL), Computers and Society (cs.CY), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models},
  publisher = {arXiv},
  year = {2023},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```


[**Paper on ArXiv**](https://arxiv.org/abs/2302.12173) [(PDF direct link)](https://arxiv.org/pdf/2302.12173.pdf)
