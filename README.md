# ChatGPT standard

Repository for research.

## Description

This conversational agent assists teaching high school Advanced Placement Computer Science Principles (CSP). This is a standard implementation of ChatGPT to use as a baseline for comparison.

## Getting Started

To run this locally, follow the below build instructions.

### Built With (Dependencies)

* Python >=3.9
* LangChain
* Streamlit
* OpenAI (gpt-4 model)
* Tiktoken
* ChromaDB

### Installing

1. Get an OPENAI API free API Key
2.  Clone the repository
```sh
git clone https://github.com/fraziermatthew/chatcsp.git
```
3. Install dependencies
```sh
pip install -r requirements.txt
```
4.  Add your OPENAI_API_KEY on line 12 of utils.py
```python
openai.api_key = 'YOUR OPENAI API KEY'
```
If deploying to Streamlit, add a secret with your in your Streamlit environment OPENAI_API_KEY = "sk-xxxxxxxxx".

### Execution

Running the program locally:
`streamlit run app.py`
