
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const chatMessages = document.getElementById("chat-messages");
const sendButton = chatForm.querySelector("button");

/* Automatically resize the question box */
function resizeQuestionInput() {
    questionInput.style.height = "auto";

    const maxHeight = 300;
    const newHeight = Math.min(
        questionInput.scrollHeight,
        maxHeight
    );

    questionInput.style.height = `${newHeight}px`;
    questionInput.style.overflowY =
        questionInput.scrollHeight > maxHeight ? "auto" : "hidden";
}


questionInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        // Submit only when a question has been entered
        if (questionInput.value.trim() && !sendButton.disabled) {
            sendButton.click();
        }
    }
});


/* Add a message to the chat */
function addMessage(text, className) {
    const message = document.createElement("div");

    message.classList.add("message", className);
    message.textContent = text;

    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}

/* Submit the question to the backend */
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "user-message");

    const loadingMessage = addMessage(
        "Thinking...",
        "bot-message"
    );

    questionInput.value = "";
    resizeQuestionInput();

    questionInput.disabled = true;
    sendButton.disabled = true;

    try {
        const response = await fetch("https://portfolio-ai-assistant-project.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "The chatbot request failed."
            );
        }

        if (data.error || !data.answer?.trim()) {
            throw new Error(
                data.error || "The AI returned an empty answer."
            );
        }

        loadingMessage.innerHTML = DOMPurify.sanitize(
            marked.parse(data.answer)
        );

    } catch (error) {
        console.error("Chat error:", error);

        loadingMessage.textContent =
            error.message === "Failed to fetch"
                ? "Unable to connect to the chatbot. Please try again."
                : `Sorry, the chatbot encountered an error: ${error.message}`;

    } finally {
        questionInput.disabled = false;
        sendButton.disabled = false;
        questionInput.focus();
        resizeQuestionInput();
        chatMessages.scrollTop = chatMessages.scrollHeight;
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
} catch (error) {
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
    } catch (error) {
        console.warn("Theme preference could not be saved.");
    }
});
