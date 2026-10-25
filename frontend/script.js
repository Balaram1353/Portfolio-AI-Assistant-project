
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const chatMessages = document.getElementById("chat-messages");
const sendButton = chatForm.querySelector('button[type="submit"]');

const API_URL =
    "https://portfolio-ai-assistant-project.onrender.com/chat";

const REQUEST_TIMEOUT_MS = 120_000;

const STATUS_MESSAGES = [
    "Connecting to the AI service...",
    "Preparing your question...",
    "Generating your answer...",
    "Still working on your response...",
    "Almost there..."
];

/* Automatically resize the question box */
function resizeQuestionInput() {
    questionInput.style.height = "auto";

    const maxHeight = 180;
    const newHeight = Math.min(questionInput.scrollHeight, maxHeight);

    questionInput.style.height = `${newHeight}px`;
    questionInput.style.overflowY =
        questionInput.scrollHeight > maxHeight ? "auto" : "hidden";
}

questionInput.addEventListener("input", resizeQuestionInput);

questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        if (questionInput.value.trim() && !sendButton.disabled) {
            chatForm.requestSubmit();
        }
    }
});

/* Add a plain-text chat message */
function addMessage(text, className) {
    const message = document.createElement("div");
    message.classList.add("message", className);
    message.textContent = text;

    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}

/* Create an animated loading message */
function addLoadingMessage() {
    const message = document.createElement("div");
    message.classList.add("message", "bot-message", "loading-message");
    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");

    message.innerHTML = `
        <span class="loading-spinner" aria-hidden="true"></span>
        <span class="loading-copy">
            <span class="loading-title">Working on your answer</span>
            <span class="loading-status">Connecting to the AI service...</span>
            <span class="loading-dots" aria-hidden="true">
                <span></span><span></span><span></span>
            </span>
        </span>
    `;

    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const statusElement = message.querySelector(".loading-status");
    let currentStatus = 0;

    const statusTimer = window.setInterval(() => {
        currentStatus = (currentStatus + 1) % STATUS_MESSAGES.length;
        statusElement.textContent = STATUS_MESSAGES[currentStatus];
    }, 3000);

    return {
        element: message,
        stop() {
            window.clearInterval(statusTimer);
        }
    };
}

/* Render a model response as sanitized Markdown */
function renderAnswer(element, answer) {
    element.classList.remove("loading-message");

    const renderedMarkdown = marked.parse(answer);
    element.innerHTML = DOMPurify.sanitize(renderedMarkdown);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* Submit a question to the backend */
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question || sendButton.disabled) {
        return;
    }

    addMessage(question, "user-message");

    const loading = addLoadingMessage();
    const loadingMessage = loading.element;

    questionInput.value = "";
    resizeQuestionInput();

    questionInput.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = "Waiting...";

    const controller = new AbortController();
    let timedOut = false;

    const timeoutId = window.setTimeout(() => {
        timedOut = true;
        controller.abort();
    }, REQUEST_TIMEOUT_MS);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question }),
            signal: controller.signal
        });

        const responseText = await response.text();
        let data;

        try {
            data = JSON.parse(responseText);
        } catch {
            throw new Error(
                "The server returned an unexpected response. Please try again."
            );
        }

        if (!response.ok) {
            const detail =
                typeof data.detail === "string"
                    ? data.detail
                    : "The chatbot request failed.";

            throw new Error(detail);
        }

        if (
            typeof data.answer !== "string" ||
            !data.answer.trim()
        ) {
            throw new Error(
                data.error || "The AI returned an empty answer."
            );
        }

        loading.stop();
        renderAnswer(loadingMessage, data.answer);

    } catch (error) {
        console.error("Chat error:", error);

        loading.stop();

        let userMessage;

        if (timedOut) {
            userMessage =
                "This request is taking longer than expected and was stopped. Please try again.";
        } else if (error.name === "AbortError") {
            userMessage = "The request was cancelled. Please try again.";
        } else if (error.message === "Failed to fetch") {
            userMessage =
                "Unable to connect to the chatbot. The service may be starting up. Please try again shortly.";
        } else {
            userMessage = `Sorry, I couldn't complete your request. ${error.message}`;
        }

        loadingMessage.classList.remove("loading-message");
        loadingMessage.textContent = userMessage;

    } finally {
        window.clearTimeout(timeoutId);
        loading.stop();

        questionInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = "Send";

        resizeQuestionInput();
        chatMessages.scrollTop = chatMessages.scrollHeight;
        questionInput.focus();
    }
});

/* =========================================
   LIGHT / DARK MODE
   ========================================= */

const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");
const themeLabel = document.getElementById("theme-label");

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;

    const isLight = theme === "light";

    themeIcon.textContent = isLight ? "☾" : "☀";
    themeLabel.textContent = isLight ? "Dark mode" : "Light mode";

    themeToggle.setAttribute(
        "aria-label",
        isLight ? "Switch to dark mode" : "Switch to light mode"
    );
}

let savedTheme = "dark";

try {
    const storedTheme = localStorage.getItem("portfolio-theme");

    if (storedTheme === "light" || storedTheme === "dark") {
        savedTheme = storedTheme;
    }
} catch {
    console.warn("Theme preference could not be loaded.");
}

applyTheme(savedTheme);

themeToggle.addEventListener("click", () => {
    const currentTheme =
        document.documentElement.dataset.theme || "dark";

    const nextTheme = currentTheme === "dark" ? "light" : "dark";

    applyTheme(nextTheme);

    try {
        localStorage.setItem("portfolio-theme", nextTheme);
    } catch {
        console.warn("Theme preference could not be saved.");
    }
});
