from agents.analysis_agent import analyze_report
from agents.diet_agent import generate_diet_plan
from agents.exercise_agent import generate_exercise_plan


def run_pipeline(data):
    # -----------------------------
    # STEP 1: ANALYSIS
    # -----------------------------
    analysis = analyze_report(data)

    # -----------------------------
    # STEP 2: EXTRACT SUMMARY
    # -----------------------------
    summary = analysis.get("summary", "")
    analysis_clean = dict(analysis)
    analysis_clean.pop("summary", None)

    # -----------------------------
    # STEP 3: DIET
    # -----------------------------
    diet = generate_diet_plan(analysis_clean)

    # -----------------------------
    # STEP 4: EXERCISE
    # -----------------------------
    exercise = generate_exercise_plan(analysis_clean)

    # -----------------------------
    # STEP 5: FINAL STRUCTURE
    # -----------------------------
    return {
        "analysis": analysis_clean,
        "diet": diet,
        "exercise": exercise,
        "summary": summary
    }