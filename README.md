🧠 Infera AI Agent

An agentic multi-modal AI system that processes text, images, PDFs, and audio inputs simultaneously, understands user intent, and autonomously executes the correct sequence of tools to produce structured, text-only outputs.

Built as part of a Generative AI Internship Assignment, this project demonstrates real-world LLM orchestration, tool chaining, and multi-input reasoning similar to ChatGPT-style agents.

🚀 Live Demo

🔗 [Add your deployed URL here]

📌 Key Features
🔹 Multi-Modal Input Support
📝 Text queries (plain or structured)
🖼️ Image input → OCR-based text extraction
📄 PDF files → text extraction + OCR fallback for scanned docs
🎧 Audio files → Speech-to-Text conversion
🔗 Multiple inputs in a single request
🔹 Agentic Capabilities
Intelligent intent detection across multiple inputs
Autonomous multi-step tool planning
Cross-input reasoning (PDF + audio + query together)
Automatic clarification questions when input is ambiguous
🔹 Core Functionalities
📄 OCR for images and PDFs
🎥 YouTube URL detection + transcript extraction
🧾 Smart summarization (1-line, bullet points, detailed summary)
😊 Sentiment analysis with confidence score
💻 Code explanation + bug detection + time complexity analysis
🎧 Audio transcription + summarization
🔗 Cross-document reasoning and comparison
🧠 Agent Behavior

The agent follows strict reasoning rules:

❗ If input is unclear → asks a follow-up question
🧩 Breaks tasks into minimal tool steps
⚙️ Executes tools automatically without user micromanagement
📤 Returns only clean, structured text output
🧾 Provides optional execution trace / reasoning steps
🏗️ System Architecture
User Input (Text / Image / PDF / Audio)
                │
                ▼
      Input Processing Layer
 (OCR / PDF Parser / STT Engine)
                │
                ▼
        Intent Understanding (LLM)
                │
                ▼
         Agent Planner (LLM Core)
                │
                ▼
         Tool Execution Engine
 (OCR | Whisper | YouTube | NLP Tools)
                │
                ▼
         Response Formatter Layer
                │
                ▼
     Final Structured Text Output
🧰 Tech Stack
Backend: FastAPI
Frontend: Streamlit / React (Chat UI)
LLM: Groq / OpenAI API
OCR: Tesseract / EasyOCR
Speech-to-Text: Whisper
PDF Processing: PyMuPDF / pdfplumber
Deployment: Docker, Render / Cloud platforms
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/arpitadhage/Infera-AI-Agent.git
cd Infera-AI-Agent
2️⃣ Create Virtual Environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in root directory:

GROQ_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
YOUTUBE_API_KEY=your_api_key_here
▶️ Run the Project
Start Backend (FastAPI)
uvicorn main:app --reload
Start Frontend (if applicable)
streamlit run app.py
🐳 Docker Setup
Build Image
docker build -t infera-ai-agent .
Run Container
docker run -p 8000:8000 infera-ai-agent
🧪 Sample Test Cases
✅ 1. Audio Understanding

Input: Audio lecture
Output:

Transcript
1-line summary
3 bullet points
5-line summary
✅ 2. PDF Question Answering

Input: PDF + “What are the action items?”
Output: Extracted action items only

✅ 3. Image Code Explanation

Input: Screenshot of code
Output:

Code explanation
Language detection
Bug detection
Time complexity
✅ 4. Cross-Input Reasoning

Input: PDF containing YouTube link + query
Output:

Extract URL
Fetch transcript
Summarize video
✅ 5. Multi-File Comparison

Input: Audio + PDF + query
Output:

Compare both sources
Final analytical answer
🧩 Design Decisions
Modular tool-based architecture
LLM acts only as planner, not executor
Strict no hallucination policy
Clean separation of:
Input processing
Reasoning engine
Tool execution
Output formatting
Easily extensible for new tools
📊 Evaluation Mapping
Criterion	Implementation
Correctness	Multi-modal processing + accurate outputs
Autonomy	LLM-based planning with tool chaining
Robustness	Error handling + fallback mechanisms
Explainability	Execution trace support
Code Quality	Modular FastAPI structure
UX	Chat-style interface + file upload
Bonus	Extensible for streaming & cost estimation
💡 Bonus Features (If Implemented)
⚡ Streaming responses
📊 Tool execution visualization
💰 Token/cost estimation before execution
🔍 Debug / reasoning trace view


👨‍💻 Author
Arpit Dhage

