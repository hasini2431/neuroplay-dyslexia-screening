const signupForm =
    document.getElementById("signupForm");

const message =
    document.getElementById("message");


signupForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;

        const age =
            Number(
                document.getElementById("age").value
            );

        const gender =
            document.getElementById("gender").value;

        const nativelang =
            document.getElementById("nativelang").value;

        const otherlang =
            document.getElementById("otherlang").value;


        if (age < 7 || age > 17) {

            message.textContent =
                "Age must be between 7 and 17.";

            message.style.color = "red";

            return;
        }


        try {

            const response =
                await fetch(
                    "https://neuroplay-dyslexia-screening.onrender.com/signup",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            username: username,

                            password: password,

                            age: age,

                            gender: gender,

                            nativelang: nativelang,

                            otherlang: otherlang

                        })
                    }
                );


            const data =
                await response.json();


            if (data.success) {

                message.textContent =
                    "Account created successfully! 🎉";

                message.style.color =
                    "green";


                signupForm.reset();


                setTimeout(
                    function() {

                        window.location.href =
                            "../index.html";

                    },
                    1500
                );

            }

            else {

                message.textContent =
                    data.message;

                message.style.color =
                    "red";

            }

        }

        catch (error) {

            console.error(error);

            message.textContent =
                "Cannot connect to the backend. Make sure FastAPI is running.";

            message.style.color =
                "red";

        }

    }
);