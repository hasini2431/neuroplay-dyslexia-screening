import joblib
import os


# -------------------------------------------------
# Load the trained XGBoost models
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "dyslexia_age_specific_xgboost_models.pkl"
)

model_package = joblib.load(MODEL_PATH)


# -------------------------------------------------
# Build features for XGBoost
# -------------------------------------------------

def build_features(age_group, answers, user_info):

    # Convert age group to the key used inside the PKL file
    #
    # 7-8   -> age_7_8
    # 9-11  -> age_9_11
    # 12-17 -> age_12_17

    model_key = f"age_{age_group.replace('-', '_')}"

    # Get the correct age-specific model information
    model_data = model_package[model_key]

    # Get the exact feature order expected by the model
    required_features = model_data["features"]

    # Dictionary to store all features
    features = {}

    # -------------------------------------------------
    # User information
    # -------------------------------------------------

    features["Gender"] = user_info.get(
        "Gender",
        "Female"
    )

    features["Nativelang"] = user_info.get(
        "Nativelang",
        "Telugu"
    )

    features["Otherlang"] = user_info.get(
        "Otherlang",
        "No"
    )

    features["Age"] = user_info.get(
        "Age"
    )

    # -------------------------------------------------
    # Question features
    # -------------------------------------------------

    for question_id, result in answers.items():

        qid = int(question_id)

        features[f"Clicks{qid}"] = result.get(
            "clicks",
            0
        )

        features[f"Hits{qid}"] = result.get(
            "hits",
            0
        )

        features[f"Misses{qid}"] = result.get(
            "misses",
            0
        )

        features[f"Score{qid}"] = result.get(
            "score",
            0
        )

        features[f"Accuracy{qid}"] = result.get(
            "accuracy",
            0
        )

        features[f"Missrate{qid}"] = result.get(
            "missrate",
            0
        )

    # -------------------------------------------------
    # Arrange features in EXACT model order
    # -------------------------------------------------

    final_features = {}

    for feature in required_features:

        final_features[feature] = features.get(
            feature,
            0
        )

    return final_features