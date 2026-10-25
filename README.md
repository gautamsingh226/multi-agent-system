🔬 Multi-Agent Research Assistant

An AI-powered research assistant that uses multiple agents to search the web, analyze information, generate reports, and evaluate their quality through a Streamlit interface.


# 🔬 Multi-Agent Research Assistant

**An AI-powered research assistant that uses multiple agents to search the web, analyze information, generate reports, and evaluate their quality through a Streamlit interface.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-AI%20Agents-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-red?logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-purple)


---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation Instructions](#-installation-instructions)
- [How to Run the Streamlit Application](#-how-to-run-the-streamlit-application)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [Future Improvements](#-future-improvements)

---

## 📖 Project Overview

The **Multi-Agent Research Assistant** is an AI-powered application built with Python, LangChain, OpenRouter, and Streamlit.

It automates the research process by using multiple AI agents and chains to collect information from the web, extract relevant content, generate structured research reports, and evaluate the quality of those reports.

Instead of manually searching through multiple websites and organizing information, users can enter a research topic and let the system perform the research workflow.

The application provides an interactive Streamlit interface where users can enter research topics, view generated reports, inspect intermediate results, and download the final output.

### 🎯 Project Objective

The main objective of this project is to simplify web research by automating information gathering, report generation, and quality evaluation using AI.

---

## ✨ Features

- **🔍 Web Search:** Searches the web for relevant information about a given research topic.
- **📄 Content Extraction:** Extracts useful content from webpages for further analysis.
- **🤖 Multi-Agent Workflow:** Uses different agents and chains for searching, reading, writing, and reviewing information.
- **✍️ AI Report Generation:** Generates structured research reports based on the collected information.
- **⚖️ AI-Powered Review:** Evaluates the generated report, provides a quality score, identifies weaknesses, and suggests improvements.
- **🌐 Interactive Streamlit UI:** Provides a simple web interface for interacting with the research assistant.
- **📊 Intermediate Results:** Allows users to inspect the different stages of the research process.
- **💾 Research Caching:** Can reuse cached research results to reduce repeated processing for the same query.
- **📥 Report Export:** Supports downloading reports in formats such as TXT, Markdown, and JSON, if implemented in the application.
- **⚡ Automated Workflow:** Reduces the manual effort required to research a topic and prepare a report.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web-based user interface |
| LangChain | AI agent and workflow development |
| LangChain Core (LCEL) | Building language model processing chains |
| LangChain OpenAI | Connecting language models through an OpenAI-compatible API |
| OpenRouter API | Accessing supported AI language models |
| Tavily Search API | Searching the web for research information |
| Requests | Sending HTTP requests |
| BeautifulSoup | Extracting text from HTML webpages |
| python-dotenv | Loading environment variables from a `.env` file |
| Hashlib | Generating hashes for cache keys |
| Pickle | Storing cached Python objects |

---

## 📁 Project Structure

The project may be organized as follows:

multi-agent-system/
│
├── app.py                 # Streamlit application
├── agents.py              # AI agents and research workflow
├── tools.py               # Web search and webpage extraction tools
├── requirements.txt       # Python dependencies
├── .env                   # API keys (keep private)
├── .env.example           # Example environment configuration
├── .gitignore             # Files excluded from Git
└── .research_cache/       # Locally cached research results


**Note:** The structure above is a reference. Keep the filenames and folders consistent with your actual project.

---

## ⚙️ Installation Instructions

Follow these steps to install and configure the project on your computer.

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- Git
- A code editor such as VS Code
- An OpenRouter API key
- A Tavily API key, if your project uses Tavily for web search

### Step 1: Clone the Repository

Replace `<your-username>` with your GitHub username.
git clone https://github.com/<your-username>/multi-agent-system.git

Navigate to the project directory:
cd multi-agent-system


If you have already downloaded or cloned the project, open a terminal in the project directory instead.

### Step 2: Create a Virtual Environment

Create an isolated Python environment:
python -m venv venv


### Step 3: Activate the Virtual Environment

**Windows PowerShell:**
.\venv\Scripts\Activate.ps1

**Windows Command Prompt:**
venv\Scripts\activate.bat

**macOS/Linux:**
source venv/bin/activate

### Step 4: Install Dependencies

Upgrade pip:
python -m pip install --upgrade pip

Install the required packages:
pip install -r requirements.txt


**Important:** Make sure your `requirements.txt` file contains all the Python packages imported by your project.

If you do not have a `requirements.txt` file yet, create one containing the dependencies your code actually uses.

### Step 5: Configure Environment Variables

Create a file named `.env` in the root directory of the project.

If your project contains a `.env.example` file, you can copy it.

**Windows PowerShell:**

Copy-Item .env.example .env

Alternatively, create `.env` manually.

Add your API keys using the environment variable names expected by your Python code.

For example:

OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

Replace the placeholder values with your actual API keys.

- Get your OpenRouter API key from the [OpenRouter website](https://openrouter.ai/keys).
- Get your Tavily API key from the [Tavily website](https://tavily.com/).

**Security Warning:** Never upload your `.env` file or API keys to GitHub. Add `.env` to your `.gitignore` file.

---

## 🚀 How to Run the Streamlit Application

After installing the dependencies and configuring your API keys, follow these steps.

### Step 1: Open the Project Directory

Open your terminal in the project folder:

cd multi-agent-system


Activate your virtual environment if it is not already active.

### Step 2: Start the Streamlit Application

Run the following command:
streamlit run app.py


This starts the Streamlit development server.

### Step 3: Open the Application in Your Browser

Streamlit normally opens the application automatically in your default browser.

If it does not, open:
http://localhost:8501


### Step 4: Use the Application

1. Enter a research topic in the input field.
2. Start the research process using the button provided by the application.
3. Allow the agents to search for information and process the results.
4. Review the generated research report.
5. Inspect intermediate results and review feedback if these features are available.
6. Download the report in a supported format if the application provides export options.

**To stop the application**, return to the terminal and press:
Ctrl + C

---

## 🔄 How It Works

The research assistant follows a multi-stage workflow.

### 1. Search Agent

Searches the web for information relevant to the user's research topic.

### 2. Reader Agent

Extracts relevant content from selected webpages.

### 3. Writer Chain

Uses the collected information to generate a structured research report.

### 4. Critic Chain

Evaluates the generated report, identifies weaknesses, and provides suggestions for improvement.

### Workflow Diagram

       User Research Topic
                |
                v
          Search Agent
                |
                v
          Reader Agent
                |
                v
          Writer Chain
                |
                v
          Critic Chain
                |
                v
      Final Research Report
                |
                v
        User Reviews Output

---

## 🔐 Configuration

The application uses environment variables to store API credentials.

Example `.env` configuration:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Make sure that:

- Your API keys are valid.
- Your `.env` file is in the project root directory.
- Your application loads environment variables correctly.
- The environment variable names match those used in your Python code.
- Your `.env` file is excluded from version control.

### Recommended `.gitignore`

```gitignore
.env
venv/
__pycache__/
*.py[cod]
.research_cache/
.streamlit/secrets.toml
```

---

## 🔮 Future Improvements

Possible improvements for the project include:

- Parallel webpage extraction for faster research.
- Iterative report improvement based on critic feedback.
- PDF export for generated reports.
- Support for selecting different language models.
- Improved source verification and citation handling.
- More detailed research history and report management.

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Push your branch to GitHub.
6. Open a Pull Request.

---

## 📄 License

No license has been specified for this project yet.

If you decide to distribute the project under the MIT License, add a `LICENSE` file containing the appropriate MIT License text and update this section accordingly.

---