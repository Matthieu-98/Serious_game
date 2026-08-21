document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("chatbot-toggle");
    const close = document.getElementById("chatbot-close");
    const windowBox = document.getElementById("chatbot-window");

    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");

    if (!toggle || !windowBox || !form) {
        return;
    }


    toggle.addEventListener("click", function () {
        windowBox.classList.remove("chatbot-hidden");
        input.focus();
    });


    close.addEventListener("click", function () {
        windowBox.classList.add("chatbot-hidden");
    });


    function addMessage(text, type) {

        const div = document.createElement("div");

        div.classList.add(
            type === "user"
                ? "user-message"
                : "bot-message"
        );

        div.textContent = text;

        messages.appendChild(div);

        messages.scrollTop = messages.scrollHeight;
    }


    function getCsrfToken() {

        const csrfInput = document.querySelector(
            "#chatbot-form input[name='csrfmiddlewaretoken']"
        );

        return csrfInput ? csrfInput.value : "";
    }


    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const message = input.value.trim();

        if (!message) {
            return;
        }

        addMessage(message, "user");

        input.value = "";
        input.disabled = true;

        const loading = document.createElement("div");
        loading.className = "bot-message";
        loading.textContent = "Je réfléchis...";
        messages.appendChild(loading);

        try {

            const response = await fetch("/chatbot/", {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded",

                    "X-CSRFToken": getCsrfToken()
                },

                body: new URLSearchParams({
                    message: message
                })
            });


            const data = await response.json();

            loading.remove();


            if (!response.ok) {

                addMessage(
                    data.error ||
                    "Une erreur est survenue.",
                    "bot"
                );

                return;
            }


            addMessage(data.reply, "bot");

        } catch (error) {

            loading.remove();

            addMessage(
                "Impossible de contacter le guide pour le moment.",
                "bot"
            );

        } finally {

            input.disabled = false;
            input.focus();
        }

    });

});