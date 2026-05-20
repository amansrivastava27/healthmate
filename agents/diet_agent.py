def generate_diet_plan(analysis):
    plan = []

    # -----------------------------
    # BASIC CONDITIONS
    # -----------------------------
    if analysis.get("hemoglobin", {}).get("status") == "low":
        plan.append("Eat iron-rich foods like spinach, beetroot, jaggery")
        plan.append("Include vitamin C (lemon, orange) for better absorption")

    if analysis.get("glucose", {}).get("status") == "high":
        plan.append("Avoid sugar and sweets")
        plan.append("Eat whole grains, vegetables, and fiber-rich foods")

    if analysis.get("cholesterol", {}).get("status") == "high":
        plan.append("Avoid fried and oily food")
        plan.append("Eat oats, nuts, and healthy fats")

    if analysis.get("vitamin_b12", {}).get("status") == "low":
        plan.append("Drink milk, Eat eggs, paneer, and fortified cereals")

    if analysis.get("vitamin_d", {}).get("status") == "low":
        plan.append("Get sunlight exposure and eat vitamin D rich foods")

    # -----------------------------
    # THYROID
    # -----------------------------
    if analysis.get("thyroid", {}).get("status") == "hypothyroidism":
        plan.append("Use iodized salt and eat nuts and seeds")

    if analysis.get("thyroid", {}).get("status") == "hyperthyroidism":
        plan.append("Avoid caffeine and processed food")

    # -----------------------------
    # DIABETES
    # -----------------------------
    if "diabetes" in analysis:
        plan.append("Follow low sugar diet and eat small frequent meals")

    # -----------------------------
    # PCOD
    # -----------------------------
    if "pcod_risk" in analysis:
        plan.append("Avoid junk food and eat high fiber diet")

    # -----------------------------
    # LIVER / KIDNEY
    # -----------------------------
    if "liver_issue" in analysis:
        plan.append("Avoid alcohol and fatty food")

    if "kidney_issue" in analysis:
        plan.append("Reduce salt intake and stay hydrated")

    # -----------------------------
    # INFECTIONS
    # -----------------------------
    if analysis.get("typhoid", {}).get("status") == "positive":
        plan.append("Eat light food like khichdi and soups")

    if analysis.get("dengue", {}).get("status") == "positive":
        plan.append("Drink coconut water and stay hydrated")

    if analysis.get("malaria", {}).get("status") == "positive":
        plan.append("Eat light nutritious food and drink fluids")

    if analysis.get("covid", {}).get("status") == "positive":
        plan.append("Eat immunity boosting foods like turmeric milk")

    # -----------------------------
    # DEFAULT
    # -----------------------------
    if not plan:
        plan.append("Maintain a balanced diet with fruits and vegetables")

    # Remove duplicates
    plan = list(set(plan))

    return plan