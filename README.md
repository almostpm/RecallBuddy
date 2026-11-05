# 🧠 RecallBuddy — Your Personal AI Tutor (link - https://recallbuddy-ul60.onrender.com/)

**RecallBuddy** is an AI-powered study buddy that instantly turns any text or PDF into a fun, interactive quiz game. Instead of just reading the same pages over and over, RecallBuddy reads the material for you and tests your memory. It is like having a super-smart digital tutor right on your computer screen.

---

## 📖 Table of Contents
1. [How It Helps You Learn Faster](#how-it-helps-you-learn-faster)
2. [Project Workflow (How it works behind the scenes)](#project-workflow)
3. [Application Interface](#application-interface)
4. [How to Use RecallBuddy](#how-to-use-recallbuddy)
5. [How to Run This Project on Your Computer](#how-to-run-this-project-on-your-computer)
6. [Tech Stack (For Developers)](#tech-stack-for-developers)

---

## 🚀 How It Helps You Learn Faster

* **Forces You to Actually Think:** Normal reading is passive—your eyes move, but your brain might not absorb it. RecallBuddy stops you and asks questions, forcing your brain to remember.
* **Stops You from Wasting Time:** Instead of re-reading a whole chapter, the AI tells you exactly what you got wrong and explains it in simple words.
* **Instant Explanations:** If you choose a wrong answer, it doesn't just say "Incorrect." It immediately explains *why* it is wrong so you learn from the mistake on the spot.
* **Tracks Your Progress:** It shows your total score and accuracy rate, acting like a fitness tracker for your brain.

---

## 🖼️ Project Workflow

*Here is a simple diagram showing how the application works from start to finish.*

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/e0e7e43f-a88d-427e-8a72-fb2d926e1f0f" />


---

## 💻 Application Interface

*RecallBuddy features a clean, modern, black-and-white "Mac OS" style design.*

<img width="1335" height="912" alt="image" src="https://github.com/user-attachments/assets/0e6e4183-1d9e-4219-8d18-0f6d75127870" />
<img width="1396" height="956" alt="image" src="https://github.com/user-attachments/assets/f294ce6b-f2e1-4033-ad21-ce94d5ece179" />
<img width="1322" height="862" alt="image" src="https://github.com/user-attachments/assets/f717380f-5b2f-4884-af77-11d99916f7cf" />
<img width="1381" height="845" alt="image" src="https://github.com/user-attachments/assets/3c00dff7-9a24-4eec-b95b-688876be7f4c" />
<img width="1331" height="850" alt="image" src="https://github.com/user-attachments/assets/02a5a901-cacd-4b1d-b022-0d4578488912" />

---

## 🎮 How to Use RecallBuddy

1. **Upload Your Material:** Click on "Choose File" to upload a PDF (like a textbook chapter or notes). Alternatively, you can just copy-paste your text into the large text box.
2. **Generate the Game:** Click the big black **"GENERATE TRIVIA GAME"** button.
3. **Wait a Moment:** The AI will read your text and create a custom question.
4. **Answer and Learn:** Select the correct option (A, B, C, or D). The app will instantly tell you if you are right and explain the answer.
5. **Check Your Score:** Look at the top right of the quiz box to see your score, and keep playing to improve your accuracy!

---

## 🛠️ How to Run This Project on Your Computer

If you want to run this project locally on a Windows PC, follow these simple steps:

**Step 1: Download the Project**
Download this repository as a ZIP file and extract it to a folder.

**Step 2: Get a Free AI Key**
This app uses Groq for AI. You need a free API key.
1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up and create an API Key.
3. Inside the project folder, create a new file named exactly `.env` (no .txt at the end).
4. Open the `.env` file in Notepad and paste this line:
   `GROQ_API_KEY=your_copied_api_key_here`

**Step 3: Start the App**
1. Double-click on the file named **`start.bat`**.
2. A black terminal window will open. It will install the required packages (this may take a few minutes the first time).
3. Your web browser will automatically open, and RecallBuddy will be ready to use!

---

## ⚙️ Tech Stack (For Developers)

While this README is for general users, here is the technical magic that makes it work:
* **Backend:** Python, FastAPI
* **Frontend:** HTML, CSS, JavaScript (Custom UI)
* **AI Engine:** Groq API (for generating questions and explanations)
* **Text Processing:** PDF parsing with `pypdf` and lightweight local embeddings using `FastEmbed`.
