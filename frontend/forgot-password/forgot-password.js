const resetForm = document.getElementById("resetForm");
const message = document.getElementById("message");

resetForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value.trim();

    const newPassword =
        document.getElementById("newPassword").value;

    const confirmPassword =
        document.getElementById("confirmPassword").value;


    // Check passwords

    if (newPassword !== confirmPassword) {

        message.textContent =
            "Passwords do not match.";

        message.style.color = "red";

        return;
    }


    // Basic password check

    if (newPassword.length < 6) {

        message.textContent =
            "Password must contain at least 6 characters.";

        message.style.color = "red";

        return;
    }


    message.textContent =
        "Resetting password...";

    message.style.color = "#6d35d4";


    try {

        const response = await fetch(
            "https://neuroplay-dyslexia-screening.onrender.com/reset-password",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    new_password: newPassword
                })
            }
        );


        const data = await response.json();


        console.log("Reset response:", data);


        if (data.success) {

            message.textContent =
                "Password reset successfully! 🎉";

            message.style.color = "green";


            resetForm.reset();


            // Go to login after 1.5 seconds

            setTimeout(function () {

                window.location.href =
                    "../login/login.html";

            }, 1500);


        } else {

            message.textContent =
                data.message;

            message.style.color = "red";
        }


    } catch (error) {

        console.error(
            "Password reset error:",
            error
        );


        message.textContent =
            "Cannot connect to the backend. Make sure FastAPI is running.";

        message.style.color = "red";
    }

});