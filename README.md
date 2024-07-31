<div align="center">
<image src="https://github.com/k-arthik-r/ai_powered_log_parsing_tool/assets/111432615/ffe862c1-086d-426b-abc1-13fe0212f4b9"/>
</div>


------------------------

<div align="center">
  <a><img src="https://custom-icon-badges.demolab.com/badge/Streamlit-000000?style=for-the-badge&logo=streamlit"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/GROQ Cloud-FFFFFF?style=for-the-badge&logo=groq"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/google colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Huggingface-FF9D00?style=for-the-badge&logo=huggingface-logo"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/Llama 3-0467DF?style=for-the-badge&logo=meta&logoColor=white"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/embedding 001-FFFFFF?style=for-the-badge&logo=google"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Transformer-gold?style=for-the-badge&logo=package&logoColor=black"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Langchain-FBEEE9?style=for-the-badge&logo=ln"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/FAISS DB-999999?style=for-the-badge&logo=faiss"></a> &nbsp;
</div>

------------------------

An advanced AI-powered solution enhances network diagnostics by leveraging large language models (LLMs). The system intelligently parses various types of device logs, including structured and unstructured data, to identify patterns and anomalies. It provides actionable insights and recommendations to help diagnose and resolve network issues efficiently. This solution simplifies the complexity of log analysis, enabling quicker and more accurate problem detection and resolution.

------------------------

## Requirments
Python 3.11.9 or Higher (Recommended) 

<a href="https://www.python.org/downloads/" alt="python">
        <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" /></a>

<br>
<br>

Create an account on groq cloud and get a Groq API Key

<a href="https://console.groq.com/keys" alt="mongo">
      <img src="https://custom-icon-badges.demolab.com/badge/GROQ Cloud-FFFFFF?style=for-the-badge&logo=groq"></a>
        
<br>
<br>

Create a google account and get a Google API Key

<a href="https://aistudio.google.com/app/apikey" alt="mongo">
      <img src="https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white"></a>

--------------------

## Modules/Libraries Used

All The Modules/Libraries Used in the Project can be installed using [requirements.txt](requirements.txt)

- streamlit~=1.35.0
- langchain~=0.2.1
- python-dotenv~=1.0.1
- langchain-groq~=0.1.4
- langchain-community~=0.2.1
- faiss-cpu~=1.8.0
- langchain-google-genai~=1.0.6


--------------------

## How to Run?

- Intialize a Git Repository.

  
``` bash
  git init
```

- Clone the Current Git Repository.
  
```bash
  git clone https://github.com/k-arthik-r/ai_powered_log_parsing_tool.git
```

- Navigate to the root Directory of the project and Create a python virtual environment.
  
```bash
  python -m venv venv

```
- Activate the Environment:

  - for Powershell

  ```bash
    .\venv\Scripts\Activate.ps1
  ```
  - for CommandPrompt

  ```bash
    .\venv\Scripts\activate.bat
  ```

- Install all the Modules Present in [requirements](requirements.txt)
  
```bash
  pip install -r requirements.txt
```

- paste your google and groq API keys inside .env file in the root directory. [Here](.env)

```bash
  GOOGLE_API_KEY = <paste your google api key here>
  GROQ_API_KEY = <paste your groq api key here>
```

- run your application using,
  
```bash
  streamlit run app.py
```

## Using Docker

- Start your Docker Engine.
- Open your Terminal (Power shell or Comand Prompt).
- Pull the Application Docker Image from the Docker Hub:
  
  ```bash
  docker pull karthikclgid/ai-powered-log-parsing-tool:latest
  ```
  
- Run the Docker Image:

  ```bash
  docker run -p 8501:8501 karthikclgid/ai-powered-log-parsing-tool:latest
  ```
  
- The Application will start its Execution.

-------------------------

## Abstract Architecture

![arche](https://github.com/k-arthik-r/ai_powered_log_parsing_tool/assets/111432615/c9da9040-4a58-460e-9bff-a8e7887ed8a7)

----------------------------

## Report

The complete details of the Project Implementation is provided in [Project Report](Report/project-report.pdf)

----------------------------

## License

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)


