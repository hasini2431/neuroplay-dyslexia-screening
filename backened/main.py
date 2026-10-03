from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
from test_logic import process_question
from pydantic import BaseModel
from auth import signup, signin, create_database, get_user,reset_password
from feature_builder import build_features, model_package

app = FastAPI(
    title="Dyslexia Screening API",
    description="Gamified dyslexia-risk screening prototype",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
create_database()


# Load questions
with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

questions = data["questions"]


@app.get("/")
def home():
    return {
        "message": "Dyslexia Screening API is running"
    }


@app.get("/questions")
def get_all_questions():
    return {
        "total_questions": len(questions),
        "questions": questions
    }


@app.get("/questions/{question_id}")
def get_question(question_id: int):

    for question in questions:

        if question["question_id"] == question_id:
            return question

    return {
        "error": "Question not found"
    }


class AnswerRequest(BaseModel):
    question_id: int
    response: list


@app.post("/test/answer")
def submit_answer(answer: AnswerRequest):

    result = process_question(
        answer.question_id,
        answer.response
    )

    return {
        "question_id": answer.question_id,
        "result": result
    }
class SignupRequest(BaseModel):
    username: str
    password: str
    age: int
    gender: str
    nativelang: str
    otherlang: str


class SigninRequest(BaseModel):
    username: str
    password: str
@app.post("/signup")
def signup_user(user: SignupRequest):

    return signup(
        user.username,
        user.password,
        user.age,
        user.gender,
        user.nativelang,
        user.otherlang
    )

    return result


@app.post("/signin")
def signin_user(user: SigninRequest):

    return signin(
        user.username,
        user.password
    )

    return result
def get_age_group(age):
    if 7 <= age <= 8:
        return "7-8"
    elif 9 <= age <= 11:
        return "9-11"
    elif 12 <= age <= 17:
        return "12-17"
    else:
        return None
@app.get("/test/start/{age}")
def start_test(age: int):

    age_group = get_age_group(age)

    if age_group is None:
        return {
            "success": False,
            "message": "Age must be between 7 and 17"
        }

    age_questions = []

    for question in questions:
        if age_group in question["age_groups"]:
            age_questions.append(question)

    return {
        "success": True,
        "age": age,
        "age_group": age_group,
        "total_questions": len(age_questions),
        "questions": age_questions
    }    
class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str
@app.post("/reset-password")
def reset_user_password(request: ResetPasswordRequest):

    return reset_password(
        request.username,
        request.new_password
    )    
from typing import Dict, Any

# Temporary storage for test sessions
test_sessions = {}


class TestSessionRequest(BaseModel):
    username: str
    age: int


@app.post("/test/session")
def create_test_session(request: TestSessionRequest):

    # Get user information from the database
    user = get_user(request.username)

    if user is None:
        return {
            "success": False,
            "message": "User not found. Please sign in first."
        }

    # Use the age stored in the database
    age = user["age"]

    # Determine age group
    age_group = get_age_group(age)

    if age_group is None:
        return {
            "success": False,
            "message": "Age must be between 7 and 17"
        }

    # Get questions for this age group
    age_questions = []

    for question in questions:

        if age_group in question["age_groups"]:
            age_questions.append(question)

    # Create test session
    test_sessions[request.username] = {
        "username": request.username,
        "age": age,
        "age_group": age_group,

        # Store actual user profile
        "gender": user["gender"],
        "nativelang": user["nativelang"],
        "otherlang": user["otherlang"],

        "answers": {}
    }

    return {
        "success": True,
        "username": request.username,
        "age": age,
        "age_group": age_group,
        "gender": user["gender"],
        "nativelang": user["nativelang"],
        "otherlang": user["otherlang"],
        "total_questions": len(age_questions),
        "message": "Test session created successfully"
    }
class AnswerSessionRequest(BaseModel):
    username: str
    question_id: int
    response: list


@app.post("/test/session/answer")
def submit_session_answer(answer: AnswerSessionRequest):

    # Check whether session exists
    if answer.username not in test_sessions:
        return {
            "success": False,
            "message": "Test session not found. Start the test first."
        }

    session = test_sessions[answer.username]

    # Check whether question belongs to the user's age group
    question = get_question(answer.question_id)

    if question is None:
        return {
            "success": False,
            "message": "Question not found."
        }

    if session["age_group"] not in question["age_groups"]:
        return {
            "success": False,
            "message": "This question is not available for this age group."
        }

    # Validate answer
    result = process_question(
        answer.question_id,
        answer.response
    )

    # Store result
    session["answers"][str(answer.question_id)] = result

    return {
        "success": True,
        "question_id": answer.question_id,
        "result": result,
        "answered_questions": len(session["answers"])
    }
class PredictionRequest(BaseModel):
    username: str
@app.post("/test/predict")
def predict_dyslexia(request: PredictionRequest):

    try:
        # -----------------------------------------
        # 1. Check whether test session exists
        # -----------------------------------------
        if request.username not in test_sessions:
            return {
                "success": False,
                "message": "Test session not found. Start the test first."
            }

        # -----------------------------------------
        # 2. Get test session
        # -----------------------------------------
        session = test_sessions[request.username]

        age = session["age"]
        age_group = session["age_group"]
        answers = session["answers"]

        # -----------------------------------------
        # 3. Get the correct model
        # -----------------------------------------
        model_key = f"age_{age_group.replace('-', '_')}"

        model_data = model_package[model_key]

        required_features = model_data["features"]

        # -----------------------------------------
        # 4. Calculate required questions
        # -----------------------------------------
        required_question_ids = set()

        for feature in required_features:

            if feature.startswith("Clicks"):
                question_id = int(feature.replace("Clicks", ""))
                required_question_ids.add(question_id)

        # -----------------------------------------
        # 5. Check completed questions
        # -----------------------------------------
        answered_question_ids = {
            int(question_id)
            for question_id in answers.keys()
        }

        missing_questions = (
            required_question_ids - answered_question_ids
        )

        if missing_questions:

            return {
                "success": False,
                "message": "Please complete all required questions before prediction.",
                "age_group": age_group,
                "answered_questions": len(answered_question_ids),
                "required_questions": len(required_question_ids),
                "missing_questions": sorted(missing_questions)
            }

        # -----------------------------------------
        # 6. User information
        # -----------------------------------------
        user_info = {
    "Gender": session["gender"],
    "Nativelang": session["nativelang"],
    "Otherlang": session["otherlang"],
    "Age": age
}

        # -----------------------------------------
        # 7. Build model features
        # -----------------------------------------
        features = build_features(
            age_group,
            answers,
            user_info
        )

        # -----------------------------------------
        # 8. Create DataFrame
        # -----------------------------------------
        import pandas as pd

        feature_df = pd.DataFrame(
            [features],
            columns=required_features
        )

        # -----------------------------------------
        # 9. Get XGBoost probability
        # -----------------------------------------
        model = model_data["model"]

        threshold = model_data["threshold"]

        probability = model.predict_proba(
            feature_df
        )[0][1]

        # -----------------------------------------
        # 10. Apply threshold
        # -----------------------------------------
        prediction = (
            1 if probability >= threshold else 0
        )

        # -----------------------------------------
        # 11. Convert prediction to result
        # -----------------------------------------
        if prediction == 1:
            result = "Dyslexia Risk Detected"
        else:
            result = "Low Dyslexia Risk"

        # -----------------------------------------
        # 12. Return result
        # -----------------------------------------
        return {
            "success": True,
            "username": request.username,
            "age": age,
            "age_group": age_group,
            "answered_questions": len(answered_question_ids),
            "required_questions": len(required_question_ids),
            "probability": round(
                float(probability),
                4
            ),
            "threshold": threshold,
            "prediction": prediction,
            "result": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": type(e).__name__,
            "message": str(e)
        }