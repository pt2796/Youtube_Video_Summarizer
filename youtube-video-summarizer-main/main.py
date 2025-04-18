from flask import Flask, request, render_template
import time
from pytube import YouTube
from tqdm import tqdm
from transformers import pipeline
import random
import os

app = Flask(__name__)

# Set up summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Set up question-answering pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


def clean_text(text):
    """Remove excessive spaces and blank lines."""
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
    return " ".join(cleaned_lines)


def download_audio(video_url, output_path="downloaded_audio.mp3"):
    """Download audio from YouTube."""
    from yt_dlp import YoutubeDL
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Audio downloaded successfully to {output_path}")


def fetch_transcription(video_url):
    """Fetch YouTube captions."""
    from youtube_transcript_api import YouTubeTranscriptApi

    video_id = YouTube(video_url).video_id
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([entry["text"] for entry in transcript])
    return text


def generate_quiz_questions(summary, total_questions=5):
    """Generate quiz questions with meaningful distractors."""
    questions = []
    sentences = summary.split(". ")  # Split summary into sentences
    sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty sentences

    if len(sentences) < total_questions:
        total_questions = len(sentences)

    for i in range(total_questions):
        context = sentences[i]
        try:
            qa_output = qa_pipeline(question="What is a key detail from this sentence?", context=context)
            correct_answer = qa_output["answer"]

            if not correct_answer or correct_answer.isspace():
                correct_answer = "Not specified"

            # Generate plausible incorrect options
            distractors = generate_distractors(correct_answer, context)
            options = distractors + [correct_answer]
            random.shuffle(options)

            questions.append(
                {
                    "question": f"Identify the key detail: {context}",
                    "choices": options,
                    "correct_answer": correct_answer,
                }
            )
        except Exception as e:
            print(f"Error generating question: {e}")
            continue

    return questions


def generate_distractors(correct_answer, context):
    """Generate three plausible distractors."""
    distractors = []
    words = context.split()
    for _ in range(3):
        distractor = " ".join(random.sample(words, min(len(words), 4)))
        if distractor not in distractors and distractor != correct_answer:
            distractors.append(distractor)
    return distractors


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_video():
    start_time = time.time()
    video_url = request.form["youtube_url"]
    try:
        # Download audio
        audio_path = "downloaded_audio.mp3"
        download_audio(video_url, audio_path)

        # Fetch transcription
        transcription = fetch_transcription(video_url)
        cleaned_transcription = clean_text(transcription)
        with open("transcription.txt", "w") as f:
            f.write(cleaned_transcription)

        # Summarize transcription
        summaries = []
        chunk_size = 500
        for i in tqdm(range(0, len(cleaned_transcription), chunk_size)):
            chunk = cleaned_transcription[i : i + chunk_size]
            summary = summarizer(chunk, max_length=300, min_length=50, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        final_summary = clean_text(" ".join(summaries))
        with open("summary.txt", "w") as f:
            f.write(final_summary)

        process_time = time.time() - start_time
        return render_template(
            "result.html",
            transcription=cleaned_transcription,
            summary=final_summary,
            process_time=round(process_time, 2),
        )
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        summary = request.form.get("summary", "")
        if not summary.strip():
            return "Error: No valid summary found.", 400

        total_questions = 5
        questions = generate_quiz_questions(summary, total_questions)

        if not questions:
            return "Error: No quiz questions generated.", 400

        return render_template("quiz.html", questions=questions)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    try:
        results = []
        correct_count = 0
        total_questions = int(request.form.get("total_questions", 0))

        for i in range(total_questions):
            user_answer = request.form.get(f"q{i}") or "None"
            question = request.form.get(f"question_{i}") or "Unknown Question"
            correct_answer = request.form.get(f"correct_answer_{i}") or "None"

            is_correct = user_answer.strip() == correct_answer.strip()
            if is_correct:
                correct_count += 1

            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })

        return render_template(
            "quiz_result.html",
            results=results,
            correct_count=correct_count,
            total_questions=total_questions
        )
    except Exception as e:
        return f"An error occurred: {str(e)}", 500




if __name__ == "__main__":
    app.run(debug=True)