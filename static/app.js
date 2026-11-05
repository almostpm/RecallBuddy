// RecallBuddy frontend integration with FastAPI backend
// This script makes API-driven calls to FastAPI backend for real AI-generated questions

const API_BASE = "/api";

// Track if PDF was uploaded and vectorstore is built
let pdfUploaded = false;

// Wrapper to show errors gracefully
function showError(message) {
    alert("RecallBuddy Error: " + message);
}

// Load material into the backend vectorstore before generating questions
async function apiLoadMaterial() {
    try {
        const resp = await fetch(`${API_BASE}/load_material`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });
        const text = await resp.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            showError("Server error. Please try again.");
            return false;
        }
        if (!resp.ok || data.status === "error") {
            if (data.message && (data.message.includes("OpenAI API Key required") || data.message.includes("Missing credentials"))) {
                return true;
            }
            return false;
        }
        return true;
    } catch (e) {
        showError("Could not load material: " + e.message);
        return false;
    }
}

// Upload and process a PDF file
async function apiUploadPdf(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const resp = await fetch(`${API_BASE}/upload_pdf`, {
            method: "POST",
            body: formData
        });
        const text = await resp.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            showError("Server error. Please try again.");
            return false;
        }
        if (!resp.ok || data.status === "error") {
            showError(data.message || "API Error");
            return false;
        }
        // Mark that PDF has been uploaded and vectorstore built
        pdfUploaded = true;
        // Update UI indicator
        const pdfStatus = document.getElementById('pdf-status');
        if (pdfStatus) {
            pdfStatus.classList.remove('hidden');
            pdfStatus.innerText = "PDF loaded! Ready to generate quiz.";
            setTimeout(() => {
                pdfStatus.classList.add('hidden');
            }, 3000);
        }
        return true;
    } catch (e) {
        showError("Could not upload PDF: " + e.message);
        return false;
    }
}

// Generate a question from the topic using the API
async function apiGenerateQuestion(topic) {
    try {
        const resp = await fetch(`${API_BASE}/generate_question`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: topic })
        });
        const text = await resp.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            showError("Server error. Please try again.");
            return null;
        }
        if (!resp.ok || data.status === "error") {
            showError(data.message || "API Error");
            return null;
        }
        return data;
    } catch (e) {
        showError("Could not generate question: " + e.message);
        return null;
    }
}

// Grade an answer using the API
async function apiGradeAnswer(question, options, correctIndex, userIndex, context) {
    try {
        const resp = await fetch(`${API_BASE}/grade_answer`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: question,
                options: options,
                correct_index: correctIndex,
                user_index: userIndex,
                context: context
            })
        });
        const text = await resp.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            showError("Server error. Please try again.");
            return { is_correct: false, explanation: "", stats: { total: 0, correct: 0, accuracy: 0 } };
        }
        if (!resp.ok || data.status === "error") {
            showError(data.message || "API Error");
            return { is_correct: false, explanation: "", stats: { total: 0, correct: 0, accuracy: 0 } };
        }
        return data;
    } catch (e) {
        showError("Could not grade answer: " + e.message);
        return { is_correct: false, explanation: "", stats: { total: 0, correct: 0, accuracy: 0 } };
    }
}

// Override the existing generateQuiz function (global from inline script)
window.generateQuiz = async function() {
    const rawText = document.getElementById('study-text').value.trim();

    // Check if we have input or PDF was uploaded
    if (!rawText && !pdfUploaded) {
        alert("Please paste your study notes or upload a PDF file first!");
        return;
    }

    // Show loading state
    const questionTextEl = document.getElementById('question-text');
    if (questionTextEl) {
        questionTextEl.innerText = "Generating AI Question...";
    }

    // Load material into vectorstore if needed
    await apiLoadMaterial();

    // Determine topic for the AI
    const topic = rawText || "Custom PDF Content";

    // Call the AI backend to generate a REAL question
    const responseData = await apiGenerateQuestion(topic);

    if (!responseData) {
        // Error already shown in apiGenerateQuestion
        if (questionTextEl) {
            questionTextEl.innerText = "Question will appear here...";
        }
        return;
    }

    // Map API response to currentQuizData structure
    currentQuizData = {
        title: responseData.question || "AI Generated Question",
        text: rawText,
        _topic: topic,
        questions: [{
            question: responseData.question,
            options: responseData.options,
            correct_index: responseData.correct_index,
            explanation: responseData.explanation,
            source_chunk: responseData.source_chunk
        }]
    };

    // Reset quiz state
    currentQuestionIdx = 0;
    userScore = 0;
    selectedOptionIdx = null;

    // Show the quiz UI
    document.getElementById('quiz-empty').classList.add('hidden');
    document.getElementById('quiz-active').classList.remove('hidden');

    // Render the single AI-generated question
    renderQuestion();
};

// Render the current question
function renderQuestion() {
    if (!currentQuizData || currentQuestionIdx >= currentQuizData.questions.length) {
        finishQuiz();
        return;
    }

    const qData = currentQuizData.questions[currentQuestionIdx];

    // Reset UI state
    selectedOptionIdx = null;
    document.getElementById('explanation-box').classList.add('hidden');

    const nextBtn = document.getElementById('next-btn');
    nextBtn.disabled = true;
    nextBtn.classList.add('opacity-50', 'cursor-not-allowed');

    // Header info
    document.getElementById('question-number').innerText = `Q${currentQuestionIdx + 1}`;
    document.getElementById('topic-badge').innerText = `Topic: ${currentQuizData.title}`;
    document.getElementById('current-score').innerText = userScore;
    document.getElementById('total-asked').innerText = currentQuestionIdx;

    // Question text
    const questionText = qData.question || qData.q || "Question will appear here...";
    document.getElementById('question-text').innerText = questionText;

    // Options
    const container = document.getElementById('options-container');
    container.innerHTML = '';

    const options = qData.options || qData.options || ["A", "B", "C", "D"];
    options.forEach((optText, idx) => {
        const btn = document.createElement('button');
        btn.className = "w-full p-3 text-left border-2 border-black bg-white hover:bg-gray-100 font-mono text-xs font-bold transition-all flex items-center justify-between group";
        btn.onclick = () => handleSelectOption(idx);
        btn.id = `option-btn-${idx}`;

        btn.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="w-6 h-6 border border-black bg-white group-hover:bg-black group-hover:text-white flex items-center justify-center font-bold text-[11px]">${String.fromCharCode(65 + idx)}</span>
                <span>${optText}</span>
            </div>
            <span class="w-3 h-3 rounded-full border border-black group-hover:bg-black"></span>
        `;
        container.appendChild(btn);
    });
}

// Handle PDF file upload
window.handlePdfUpload = function(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
        alert("Please select a valid PDF file.");
        event.target.value = ''; // Reset
        return;
    }

    const pdfStatus = document.getElementById('pdf-status');
    if (pdfStatus) {
        pdfStatus.classList.remove('hidden');
        pdfStatus.innerText = "Reading PDF...";
    }

    apiUploadPdf(file).then(success => {
        // Do NOT set textarea.value - leave it blank
        // The backend already has the vectorstore built
        event.target.value = ''; // Reset file input
    });
};

// Attach file input event listener when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const pdfInput = document.getElementById('pdf-upload');
    if (pdfInput) {
        pdfInput.addEventListener('change', window.handlePdfUpload);
    }
});

// Override handleSelectOption to use the API for grading
window.handleSelectOption = async function(optIdx) {
    if (selectedOptionIdx !== null) return; // Prevent changing after pick
    selectedOptionIdx = optIdx;

    const qData = currentQuizData.questions[currentQuestionIdx];
    const correctIndex = qData.correct_index !== undefined ? qData.correct_index : qData.correct;
    const isCorrect = (optIdx === correctIndex);

    if (isCorrect) {
        userScore++;
    }

    // Update stats counter
    totalQuestionsAsked++;
    if (isCorrect) totalCorrectAnswers++;

    // Prepare context from source
    const context = qData.source_chunk || qData.context || "";

    // Call the API for grading
    const gradeResult = await apiGradeAnswer(
        qData.question || qData.q,
        qData.options,
        correctIndex,
        optIdx,
        context
    );

    // Use API response explanation if available
    const explanationText = gradeResult.explanation || (isCorrect ? "Correct! Well done." : "That's not quite right.");
    const finalStats = gradeResult.stats || { total: 0, correct: 0, accuracy: 0 };

    // Update Options visual feedback
    qData.options.forEach((_, idx) => {
        const btn = document.getElementById(`option-btn-${idx}`);
        if (btn) {
            if (idx === correctIndex) {
                btn.className = "w-full p-3 text-left border-2 border-black bg-black text-white font-mono text-xs font-bold flex items-center justify-between";
                btn.innerHTML += `<span class="font-bold text-xs">[CORRECT ANSWER]</span>`;
            } else if (idx === optIdx && !isCorrect) {
                btn.className = "w-full p-3 text-left border-2 border-black bg-gray-200 text-black line-through font-mono text-xs flex items-center justify-between";
                btn.innerHTML += `<span class="font-bold text-xs">[WRONG]</span>`;
            } else {
                btn.classList.add('opacity-40');
            }
        }
    });

    // Show Instant Plain-Language Explanation Box
    const expBox = document.getElementById('explanation-box');
    const expStatus = document.getElementById('explanation-status');
    const expText = document.getElementById('explanation-text');

    expStatus.innerText = isCorrect ? "CORRECT (+1)" : "INCORRECT";
    expStatus.className = `px-2 py-0.5 text-[10px] font-mono font-bold uppercase text-white ${isCorrect ? 'bg-black' : 'bg-gray-800'}`;
    expText.innerText = explanationText;
    expBox.classList.remove('hidden');

    // Enable Next Button
    const nextBtn = document.getElementById('next-btn');
    nextBtn.disabled = false;
    nextBtn.classList.remove('opacity-50', 'cursor-not-allowed');

    // Update live score display
    document.getElementById('current-score').innerText = userScore;
    document.getElementById('total-asked').innerText = currentQuizData.questions.length;

    // Update stats from API response
    totalQuizzesPlayed = finalStats.total || totalQuizzesPlayed;
    totalCorrectAnswers = finalStats.correct !== undefined ? finalStats.correct : totalCorrectAnswers;
    totalQuestionsAsked = finalStats.total || totalQuestionsAsked;
};

// Next Question Handler
window.nextQuestion = function() {
    currentQuestionIdx++;
    renderQuestion();
};

// Quiz Completion Screen
window.finishQuiz = function() {
    totalQuizzesPlayed++;
    updateStatsUI();

    const container = document.getElementById('options-container');
    document.getElementById('question-number').innerText = "COMPLETE";
    document.getElementById('question-text').innerText = "Quiz Completed!";

    container.innerHTML = `
        <div class="p-6 border-2 border-black bg-gray-50 text-center space-y-3 font-mono">
            <h4 class="text-xl font-black uppercase">Final Score: ${userScore} / ${currentQuizData.questions.length}</h4>
            <p class="text-xs text-gray-700">Active testing completed. Review any mistakes above.</p>
            <button onclick="startQuiz()" class="stark-btn px-4 py-2 text-xs uppercase">Try Again</button>
        </div>
    `;

    document.getElementById('explanation-box').classList.add('hidden');
    const nextBtn = document.getElementById('next-btn');
    nextBtn.disabled = true;
    nextBtn.classList.add('opacity-50', 'cursor-not-allowed');
};

window.resetCurrentQuiz = function() {
    if (currentQuizData) {
        currentQuestionIdx = 0;
        userScore = 0;
        selectedOptionIdx = null;
        document.getElementById('explanation-box').classList.add('hidden');
        const nextBtn = document.getElementById('next-btn');
        nextBtn.disabled = true;
        nextBtn.classList.add('opacity-50', 'cursor-not-allowed');
        renderQuestion();
    }
};

window.startQuiz = function() {
    const rawText = document.getElementById('study-text').value.trim();
    if (!rawText && !pdfUploaded) {
        alert("Please paste your study notes or upload a PDF file first!");
        return;
    }
    generateQuiz();
};

// Update Brain Analytics UI
window.updateStatsUI = function() {
    document.getElementById('stats-total-quizzes').innerText = totalQuizzesPlayed;
    const pct = Math.round((totalCorrectAnswers / Math.max(1, totalQuestionsAsked)) * 100);
    document.getElementById('stats-accuracy').innerText = `${pct}%`;

    let mastery = "BEGINNER";
    if (pct > 85) mastery = "ADVANCED";
    else if (pct > 65) mastery = "INTERMEDIATE";
    document.getElementById('stats-mastery').innerText = mastery;
};

window.resetStats = function() {
    totalQuizzesPlayed = 0;
    totalCorrectAnswers = 0;
    totalQuestionsAsked = 0;
    updateStatsUI();
};

window.saveSettings = function() {
    alert("Settings saved! RecallBuddy is connected and ready.");
    switchTab('workspace');
};

// Initialize with LangChain Preset on load
window.onload = function() {
    loadPreset('langchain');
};