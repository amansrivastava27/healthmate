def generate_exercise_plan(analysis):
    plan = []

    # -----------------------------
    # CRITICAL CONDITIONS (BED REST)
    # -----------------------------
    if analysis.get("typhoid", {}).get("status") == "positive":
        return ["Complete bed rest", "Avoid physical activity"]

    if analysis.get("dengue", {}).get("status") == "positive":
        return ["Strict bed rest", "Avoid exercise until recovery"]

    if analysis.get("malaria", {}).get("status") == "positive":
        return ["Bed rest recommended", "Light movement only after recovery"]

    if analysis.get("covid", {}).get("status") == "positive":
        return ["Home rest", "Breathing exercises only"]

    # -----------------------------
    # LOW CONDITIONS (AVOID HEAVY WORKOUT)
    # -----------------------------
    if analysis.get("hemoglobin", {}).get("status") == "low":
        plan.append("Light yoga and stretching")
        plan.append("Avoid heavy workouts")

    if analysis.get("vitamin_b12", {}).get("status") == "low":
        plan.append("Light walking and stretching")

    if analysis.get("vitamin_d", {}).get("status") == "low":
        plan.append("Morning sunlight walking (15–20 mins)")

    # -----------------------------
    # HIGH CONDITIONS
    # -----------------------------
    if analysis.get("glucose", {}).get("status") == "high":
        plan.append("30-45 minutes brisk walking daily")
        plan.append("Light cardio exercises")

    if analysis.get("cholesterol", {}).get("status") == "high":
        plan.append("Cardio exercises 4-5 times/week")
        plan.append("Cycling or jogging")

    if analysis.get("uric_acid", {}).get("status") == "high":
        plan.append("Low-impact exercises like walking")
        plan.append("Avoid intense workouts")

    # -----------------------------
    # SPECIAL CONDITIONS
    # -----------------------------

    # Thyroid
    if analysis.get("thyroid", {}).get("status") == "hypothyroidism":
        plan.append("Regular walking and light strength training")

    if analysis.get("thyroid", {}).get("status") == "hyperthyroidism":
        plan.append("Yoga and relaxation exercises")

    # Diabetes
    if "diabetes" in analysis:
        plan.append("Daily walking and light exercise routine")

    # PCOD
    if "pcod_risk" in analysis:
        plan.append("Regular cardio and yoga")
        plan.append("Weight management exercises")

    # Liver
    if "liver_issue" in analysis:
        plan.append("Light physical activity like walking")

    # Kidney
    if "kidney_issue" in analysis:
        plan.append("Light exercise, avoid overexertion")

    # -----------------------------
    # DEFAULT
    # -----------------------------
    if not plan:
        plan.append("Maintain regular physical activity")
        plan.append("30 minutes walking daily")

    # Remove duplicates
    plan = list(set(plan))

    return plan