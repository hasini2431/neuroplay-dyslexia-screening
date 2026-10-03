console.log("MY LOGIN.JS IS RUNNING");
const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value;

    message.textContent = "Logging in...";
    message.style.color = "#6d35d4";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/signin",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        console.log("Response status:", response.status);

        const data = await response.json();

        console.log("Login response:", data);

        if (data.success) {

            message.textContent =
                "Login successful! 🎉";

            message.style.color = "green";

            localStorage.setItem(
                "username",
                data.username
            );

            localStorage.setItem(
                "age",
                data.age
            );

            localStorage.setItem(
                "gender",
                data.gender
            );

            localStorage.setItem(
                "nativelang",
                data.nativelang
            );

            localStorage.setItem(
                "otherlang",
                data.otherlang
            );

            setTimeout(function () {

                window.location.href =
                    "../test/test.html";

            }, 1000);

        } else {

            message.textContent =
                data.message;

            message.style.color = "red";
        }

    } catch (error) {

        console.error(
            "Login error:",
            error
        );

        message.textContent =
            "Cannot connect to the backend.";

        message.style.color = "red";
    }

});