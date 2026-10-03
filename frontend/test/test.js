// ===============================
// NeuroPlay Test JavaScript
// ===============================

const API_URL = "http://127.0.0.1:8000";


// ===============================
// Get logged-in user
// ===============================

const username = localStorage.getItem("username");
const age = localStorage.getItem("age");


// If user is not logged in
if (!username || !age) {

    alert("Please login first.");

    window.location.href = "../login/login.html";
}


// ===============================
// HTML elements
// ===============================

const usernameDisplay =
    document.getElementById("usernameDisplay");

const ageDisplay =
    document.getElementById("ageDisplay");

const questionCount =
    document.getElementById("questionCount");

const startScreen =
    document.getElementById("startScreen");

const questionScreen =
    document.getElementById("questionScreen");

const resultScreen =
    document.getElementById("resultScreen");

const startButton =
    document.getElementById("startButton");

const startMessage =
    document.getElementById("startMessage");

const questionTitle =
    document.getElementById("questionTitle");

const questionInstruction =
    document.getElementById("questionInstruction");

const gameArea =
    document.getElementById("gameArea");

const submitAnswerButton =
    document.getElementById("submitAnswerButton");

const questionMessage =
    document.getElementById("questionMessage");

const currentQuestionNumber =
    document.getElementById("currentQuestionNumber");

const progressText =
    document.getElementById("progressText");

const progressCount =
    document.getElementById("progressCount");

const progressFill =
    document.getElementById("progressFill");


// ===============================
// Test variables
// ===============================

let questions = [];

let currentQuestionIndex = 0;

let currentQuestion = null;

let currentResponse = [];


// ===============================
// Display user information
// ===============================

if (usernameDisplay) {

    usernameDisplay.textContent =
        "👤 " + username;
}

if (ageDisplay) {

    ageDisplay.textContent =
        "Age: " + age;
}


// ===============================
// Start Test
// ===============================

if (startButton) {

    startButton.addEventListener(
        "click",
        startTest
    );
}


// ===============================
// Start Test Function
// ===============================

async function startTest() {

    startButton.disabled = true;

    startMessage.textContent =
        "Preparing your test...";

    startMessage.style.color =
        "#6d35d4";


    try {

        // --------------------------------
        // Create test session
        // --------------------------------

        const sessionResponse =
            await fetch(
                `${API_URL}/test/session`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username: username,
                        age: Number(age)
                    })
                }
            );


        if (!sessionResponse.ok) {

            throw new Error(
                "Could not create test session."
            );
        }


        const sessionData =
            await sessionResponse.json();


        console.log(
            "Session:",
            sessionData
        );


        if (!sessionData.success) {

            startMessage.textContent =
                sessionData.message;

            startMessage.style.color =
                "red";

            startButton.disabled = false;

            return;
        }


        // --------------------------------
        // Get questions
        // --------------------------------

        const questionsResponse =
            await fetch(
                `${API_URL}/questions`
            );


        if (!questionsResponse.ok) {

            throw new Error(
                "Could not load questions."
            );
        }


        const questionsData =
            await questionsResponse.json();


        console.log(
            "All questions:",
            questionsData
        );


        // --------------------------------
        // Get actual question array
        // --------------------------------

        if (Array.isArray(questionsData)) {

            questions =
                questionsData;

        } else if (
            Array.isArray(
                questionsData.questions
            )
        ) {

            questions =
                questionsData.questions;

        } else {

            throw new Error(
                "Invalid questions format received from backend."
            );
        }


        // --------------------------------
        // Filter by age group
        // --------------------------------

        questions =
            questions.filter(function(question) {

                return (
                    Array.isArray(
                        question.age_groups
                    ) &&
                    question.age_groups.includes(
                        sessionData.age_group
                    )
                );

            });


        // --------------------------------
        // Remove duplicate question IDs
        // --------------------------------

        const uniqueQuestions = [];

        const questionIds = new Set();


        questions.forEach(function(question) {

            const id =
                Number(question.question_id);


            if (!questionIds.has(id)) {

                questionIds.add(id);

                uniqueQuestions.push(question);
            }

        });


        questions =
            uniqueQuestions;


        // --------------------------------
        // Sort by question ID
        // --------------------------------

        questions.sort(function(a, b) {

            return (
                Number(a.question_id) -
                Number(b.question_id)
            );

        });


        // --------------------------------
        // Console check
        // --------------------------------

        console.log(
            "Final age-specific question IDs:",
            questions.map(function(question) {

                return question.question_id;

            })
        );


        console.log(
            "Final age-specific questions:",
            questions
        );


        // --------------------------------
        // Check questions
        // --------------------------------

        if (questions.length === 0) {

            startMessage.textContent =
                "No questions found for your age group.";

            startMessage.style.color =
                "red";

            startButton.disabled = false;

            return;
        }


        // --------------------------------
        // Display question count
        // --------------------------------

        questionCount.textContent =
            questions.length;


        // --------------------------------
        // Start first question
        // --------------------------------

        currentQuestionIndex = 0;

        startScreen.classList.add(
            "hidden"
        );

        questionScreen.classList.remove(
            "hidden"
        );

        showQuestion();


    } catch (error) {

        console.error(
            "Test error:",
            error
        );


        startMessage.textContent =
            "Cannot load the test. Make sure FastAPI is running.";

        startMessage.style.color =
            "red";

        startButton.disabled = false;
    }
}


// ===============================
// Show Question
// ===============================

function showQuestion() {

    currentQuestion =
        questions[currentQuestionIndex];


    if (!currentQuestion) {

        console.error(
            "Question not found at index:",
            currentQuestionIndex
        );

        return;
    }


    // Reset response
    currentResponse = [];


    // Disable submit
    submitAnswerButton.disabled =
        true;


    // Clear message
    questionMessage.textContent =
        "";


    // --------------------------------
    // Question number
    // --------------------------------

    const questionNumber =
        currentQuestion.question_id;


    currentQuestionNumber.textContent =
        questionNumber;


    progressText.textContent =
        "Question " +
        (currentQuestionIndex + 1);


    progressCount.textContent =
        `${currentQuestionIndex + 1} / ${questions.length}`;


    // --------------------------------
    // Progress bar
    // --------------------------------

    const progress =
        (
            (currentQuestionIndex + 1) /
            questions.length
        ) * 100;


    progressFill.style.width =
        progress + "%";


    // --------------------------------
    // Question title
    // --------------------------------

    questionTitle.textContent =
        currentQuestion.task ||
        `Question ${questionNumber}`;


    // --------------------------------
    // Question instruction
    // --------------------------------

    questionInstruction.textContent =
        currentQuestion.instruction ||
        "Complete the activity below.";


    // --------------------------------
    // Create game
    // --------------------------------

    createGame(
        currentQuestion
    );
}


// ===============================
// Create Game
// ===============================

function createGame(question) {

    // Clear previous game
    gameArea.innerHTML = "";


    // =================================
    // Show question content
    // =================================

    if (question.content) {

        const content =
            document.createElement("p");

        content.className =
            "question-content";

        content.textContent =
            question.content;

        gameArea.appendChild(
            content
        );
    }


    // =================================
    // Get interaction type
    // =================================

    const type =
        question.interaction_type;


    console.log(
        "Creating game:",
        question.question_id,
        type
    );


    // =================================
    // SELF-REPORT
    // =================================

    if (
        question.response_type ===
        "self_report"
    ) {

        createSelfReportGame(
            question
        );

        return;
    }


    // =================================
    // CLICK QUESTION
    // =================================

    if (type === "click") {

        createClickGame(
            question
        );

        return;
    }


    // =================================
    // ARRANGE QUESTION
    // =================================

    if (type === "arrange") {

        createArrangeGame(
            question
        );

        return;
    }


    // =================================
    // SEQUENCE QUESTION
    // =================================

    if (type === "sequence") {

        createSequenceGame(
            question
        );

        return;
    }


    // =================================
    // AUDIO QUESTION
    // =================================

    if (
        type === "listen_and_sequence"
    ) {

        createAudioGame(
            question
        );

        return;
    }


    // =================================
    // Unknown type
    // =================================

    const error =
        document.createElement("p");

    error.textContent =
        "Unsupported question type.";

    error.style.color =
        "red";

    gameArea.appendChild(
        error
    );
}


// ===============================
// Click Game
// ===============================

function createClickGame(question) {

    const options =
        Array.isArray(question.options)
            ? question.options
            : [];


    const instruction =
        document.createElement("p");

    instruction.textContent =
        "Choose an option to continue.";

    instruction.className =
        "game-helper-text";

    gameArea.appendChild(
        instruction
    );


    options.forEach(function(option) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "game-option";

        button.textContent =
            option;


        button.addEventListener(
            "click",
            function() {

                // Remove previous selection
                document
                    .querySelectorAll(
                        ".game-option"
                    )
                    .forEach(function(btn) {

                        btn.classList.remove(
                            "selected"
                        );

                    });


                // Select option
                button.classList.add(
                    "selected"
                );


                // Save response
                currentResponse =
                    [option];


                // Enable submit
                submitAnswerButton.disabled =
                    false;

            }
        );


        gameArea.appendChild(
            button
        );

    });
}


// ===============================
// Self Report Game
// ===============================

function createSelfReportGame(question) {

    const options =
        Array.isArray(question.options)
            ? question.options
            : [];


    const instruction =
        document.createElement("p");

    instruction.textContent =
        "Choose the option that best describes your experience.";

    instruction.className =
        "game-helper-text";

    gameArea.appendChild(
        instruction
    );


    options.forEach(function(option) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "game-option";

        button.textContent =
            option;


        button.addEventListener(
            "click",
            function() {

                document
                    .querySelectorAll(
                        ".game-option"
                    )
                    .forEach(function(btn) {

                        btn.classList.remove(
                            "selected"
                        );

                    });


                button.classList.add(
                    "selected"
                );


                currentResponse =
                    [option];


                submitAnswerButton.disabled =
                    false;

            }
        );


        gameArea.appendChild(
            button
        );

    });
}


// ===============================
// Arrange Game
// ===============================

function createArrangeGame(question) {

    const items =
        Array.isArray(question.items)
            ? question.items
            : [];


    const selectedItems = [];


    const instruction =
        document.createElement("p");

    instruction.textContent =
        "Click the items in the correct order.";

    instruction.className =
        "game-helper-text";

    gameArea.appendChild(
        instruction
    );


    // Selected order display
    const selectedDisplay =
        document.createElement("div");

    selectedDisplay.className =
        "selected-order";

    gameArea.appendChild(
        selectedDisplay
    );


    items.forEach(function(item) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "game-option";

        button.textContent =
            item;


        button.addEventListener(
            "click",
            function() {

                // Don't select the same item twice
                if (
                    selectedItems.includes(
                        item
                    )
                ) {

                    return;
                }


                selectedItems.push(
                    item
                );


                button.classList.add(
                    "selected"
                );


                currentResponse =
                    selectedItems.slice();


                // Show selected order
                selectedDisplay.textContent =
                    "Your order: " +
                    selectedItems.join(
                        " → "
                    );


                // Enable when all items selected
                if (
                    selectedItems.length ===
                    items.length
                ) {

                    submitAnswerButton.disabled =
                        false;
                }

            }
        );


        gameArea.appendChild(
            button
        );

    });
}


// ===============================
// Sequence Game
// ===============================

function createSequenceGame(question) {

    const sequence =
        Array.isArray(question.sequence)
            ? question.sequence
            : [];


    if (sequence.length === 0) {

        const error =
            document.createElement("p");

        error.textContent =
            "No sequence is available for this question.";

        error.style.color =
            "red";

        gameArea.appendChild(
            error
        );

        return;
    }


    const instruction =
        document.createElement("p");

    instruction.textContent =
        "Click the items in the same order.";

    instruction.className =
        "game-helper-text";

    gameArea.appendChild(
        instruction
    );


    const selectedSequence = [];


    // Make a copy before shuffling
    const shuffled =
        sequence.slice();


    // Fisher-Yates shuffle
    for (
        let i = shuffled.length - 1;
        i > 0;
        i--
    ) {

        const j =
            Math.floor(
                Math.random() * (i + 1)
            );


        const temp =
            shuffled[i];

        shuffled[i] =
            shuffled[j];

        shuffled[j] =
            temp;
    }


    // Selected order display
    const selectedDisplay =
        document.createElement("div");

    selectedDisplay.className =
        "selected-order";

    gameArea.appendChild(
        selectedDisplay
    );


    shuffled.forEach(function(item) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "game-option";

        button.textContent =
            item;


        button.addEventListener(
            "click",
            function() {

                if (
                    selectedSequence.includes(
                        item
                    )
                ) {

                    return;
                }


                selectedSequence.push(
                    item
                );


                button.classList.add(
                    "selected"
                );


                currentResponse =
                    selectedSequence.slice();


                selectedDisplay.textContent =
                    "Your sequence: " +
                    selectedSequence.join(
                        " → "
                    );


                if (
                    selectedSequence.length ===
                    sequence.length
                ) {

                    submitAnswerButton.disabled =
                        false;
                }

            }
        );


        gameArea.appendChild(
            button
        );

    });
}


// ===============================
// Audio + Sequence Game
// ===============================

function createAudioGame(question) {

    // --------------------------------
    // Audio
    // --------------------------------

    if (question.audio_file) {

        const audio =
            document.createElement("audio");

        audio.controls = true;

        // JSON path:
        // audio/q32_Candle_Mountain_Pencil_Garden.wav
        audio.src = question.audio_file;

        gameArea.appendChild(
            audio
        );

    } else {

        const audioMessage =
            document.createElement("p");

        audioMessage.textContent =
            "Audio file is not available.";

        audioMessage.style.color =
            "red";

        gameArea.appendChild(
            audioMessage
        );
    }


    // --------------------------------
    // Display choices
    // --------------------------------

    const choices =
        Array.isArray(
            question.display_after_audio
        )
            ? question.display_after_audio
            : [];


    // Store selected order
    const selectedSequence = [];


    // --------------------------------
    // Show selected sequence
    // --------------------------------

    const selectedDisplay =
        document.createElement("div");

    selectedDisplay.className =
        "selected-order";

    selectedDisplay.textContent =
        "Your sequence: ";

    gameArea.appendChild(
        selectedDisplay
    );


    // --------------------------------
    // Create choice buttons
    // --------------------------------

    choices.forEach(function(item) {

        const button =
            document.createElement("button");

        button.type =
            "button";

        button.className =
            "game-option";

        button.textContent =
            item;


        button.addEventListener(
            "click",
            function() {

                // Prevent selecting same item twice
                if (
                    selectedSequence.includes(
                        item
                    )
                ) {
                    return;
                }


                // Add item to sequence
                selectedSequence.push(
                    item
                );


                // Highlight selected button
                button.classList.add(
                    "selected"
                );


                // Send response to backend
                currentResponse =
                    selectedSequence.slice();


                // Display selected order
                selectedDisplay.textContent =
                    "Your sequence: " +
                    selectedSequence.join(
                        " → "
                    );


                // Enable submit button
                if (
                    selectedSequence.length ===
                    choices.length
                ) {

                    submitAnswerButton.disabled =
                        false;
                }

            }
        );


        gameArea.appendChild(
            button
        );

    });
}


// ===============================
// Submit Answer
// ===============================

submitAnswerButton.addEventListener(
    "click",
    submitAnswer
);


// ===============================
// Submit Answer Function
// ===============================

async function submitAnswer() {

    if (
        !Array.isArray(currentResponse) ||
        currentResponse.length === 0
    ) {

        questionMessage.textContent =
            "Please select an answer.";

        questionMessage.style.color =
            "red";

        return;
    }


    submitAnswerButton.disabled =
        true;


    questionMessage.textContent =
        "Saving answer...";

    questionMessage.style.color =
        "#6d35d4";


    try {

        const response =
            await fetch(
                `${API_URL}/test/session/answer`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        username:
                            username,

                        question_id:
                            Number(
                                currentQuestion.question_id
                            ),

                        response:
                            currentResponse

                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Server returned HTTP " +
                response.status
            );
        }


        const data =
            await response.json();


        console.log(
            "Answer result:",
            data
        );


        if (!data.success) {

            questionMessage.textContent =
                data.message ||
                "Could not save answer.";

            questionMessage.style.color =
                "red";

            submitAnswerButton.disabled =
                false;

            return;
        }


        // --------------------------------
        // Move to next question
        // --------------------------------

        currentQuestionIndex++;


        if (
            currentQuestionIndex <
            questions.length
        ) {

            showQuestion();

        } else {

            finishTest();

        }


    } catch (error) {

        console.error(
            "Answer error:",
            error
        );


        questionMessage.textContent =
            "Could not save your answer.";

        questionMessage.style.color =
            "red";

        submitAnswerButton.disabled =
            false;
    }
}


// ===============================
// Finish Test
// ===============================

async function finishTest() {

    questionScreen.classList.add(
        "hidden"
    );


    resultScreen.classList.remove(
        "hidden"
    );


    document.getElementById(
        "resultAgeGroup"
    ).textContent =
        "Calculating...";


    document.getElementById(
        "resultQuestions"
    ).textContent =
        questions.length;


    document.getElementById(
        "riskResult"
    ).textContent =
        "Calculating...";


    try {

        const response =
            await fetch(
                `${API_URL}/test/predict`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        username:
                            username
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Prediction request failed."
            );
        }


        const data =
            await response.json();


        console.log(
            "Prediction:",
            data
        );


        if (!data.success) {

            document.getElementById(
                "riskResult"
            ).textContent =
                "Prediction unavailable";

            return;
        }


        document.getElementById(
            "resultAgeGroup"
        ).textContent =
            data.age_group;


        document.getElementById(
            "resultQuestions"
        ).textContent =
            `${data.answered_questions} / ${data.required_questions}`;
            
        document.getElementById(
             "screeningProbability"
        ).textContent =
              (Number(data.probability) * 100).toFixed(1) + "%";

        document.getElementById(
            "riskResult"
        ).textContent =
            data.result;


    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        document.getElementById(
            "riskResult"
        ).textContent =
            "Prediction unavailable";
    }
}