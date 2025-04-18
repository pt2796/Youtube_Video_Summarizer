

# 🎥 YouTube Video Summarizer & Quiz Generator

An AI-powered web app that extracts **audio** from YouTube videos, transcribes it using **OpenAI Whisper**, generates a **summary using BART**, and creates an **MCQ-based quiz using RoBERTa**. Designed to enhance **educational content consumption** by making long videos interactive, concise, and testable.

---

## 🚀 Features

- 🎧 Extracts and preprocesses audio from YouTube videos using `yt-dlp` and `FFmpeg`
- 🧠 Transcribes audio using **OpenAI Whisper**
- 📝 Summarizes the text using **facebook/bart-large-cnn**
- 🧪 Generates quizzes (5 MCQs) using **deepset/roberta-base-squad2**
- 🌐 Intuitive UI built with HTML, CSS, and Bootstrap
- 📄 Supports downloading summaries and quiz results
- 🔍 Includes a modular backend built with Flask

---

## 🧰 Technologies Used

| Component            | Technology / Library                        |
|---------------------|---------------------------------------------|
| Audio Extraction     | yt-dlp, FFmpeg                              |
| Audio Processing     | Pydub, numpy                                |
| Speech Recognition   | OpenAI Whisper (Transformer-based ASR)     |
| Text Summarization   | facebook/bart-large-cnn (HuggingFace)      |
| Quiz Generation      | deepset/roberta-base-squad2 (QA model)     |
| Backend Framework    | Flask                                       |
| Frontend             | HTML, CSS, Bootstrap, JavaScript           |
| API Tools            | requests, tqdm                              |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/ShubhangPareek/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt



⸻

🛠 Requirements

Make sure you have the following installed:
	•	Python 3.8+
	•	ffmpeg (installed & added to system PATH)
	•	Git
	•	A stable internet connection (for model loading)
	•	yt-dlp (automatically handled in the code)

⸻

🧪 How to Use

# Run the Flask app
python main.py

	1.	Open browser → go to http://127.0.0.1:5000
	2.	Paste the YouTube video link
	3.	Click “Process”
	4.	View:
	•	Full transcription
	•	Concise summary
	•	Option to Generate Quiz
	5.	Attempt the quiz
	6.	View results (Correct / Incorrect answers)

⸻

📁 Project Structure

youtube-video-summarizer/
│
├── main.py                     # Flask backend
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── index.html
│   ├── result.html
│   ├── quiz.html
│   └── quiz_result.html
├── static/                     # CSS/JS (if needed)
├── downloaded_audio.mp3        # Temporary audio file
├── transcription.txt           # Full transcript
├── summary.txt                 # Final summarized content
└── README.md                   # This file



⸻

📚 Model Overview

Task	Model Used	Framework
Transcription	openai/whisper	Whisper
Summarization	facebook/bart-large-cnn	Hugging Face
Quiz Generation	deepset/roberta-base-squad2	Hugging Face QA



⸻

📌 Notes
	•	BART uses denoising autoencoding for abstractive summarization.
	•	Whisper supports multilingual, offline, and robust noisy audio processing.
	•	RoBERTa fine-tuned on SQuAD2 provides contextual quiz generation.
	•	The system segments large audio into smaller chunks for higher accuracy and faster processing.

⸻

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

⸻

📜 License

MIT License © 2025 Shubhang Pareek

⸻
