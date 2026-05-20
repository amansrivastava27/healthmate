def get_severity(value, low, high):
    if value < low:
        return "mild" if value > low * 0.8 else "severe"
    elif value > high:
        return "mild" if value < high * 1.2 else "severe"
    return "normal"


def analyze_report(report_data):
    result = {}

    # -----------------------------
    # NORMAL RANGES
    # -----------------------------
    NORMAL_RANGES = {
        "hemoglobin": (12, 17),
        "glucose": (70, 140),
        "fasting_glucose": (70, 100),
        "cholesterol": (125, 200),
        "hdl": (40, 60),
        "ldl": (0, 100),
        "triglycerides": (0, 150),
        "tsh": (0.4, 4.0),
        "t3": (0.8, 2.0),
        "t4": (5.0, 12.0),
        "vitamin_b12": (200, 900),
        "vitamin_d": (30, 100),
        "platelets": (150000, 450000),
        "wbc": (4000, 11000),
        "rbc": (4.0, 6.0),
        "bilirubin": (0.1, 1.2),
        "creatinine": (0.6, 1.3),
        "urea": (10, 50),
        "uric_acid": (3.5, 7.2),
        "sodium": (135, 145),
        "potassium": (3.5, 5.0),
    }

    # -----------------------------
    # VALUE BASED ANALYSIS
    # -----------------------------
    for key, value in report_data.items():
        if isinstance(value, (int, float)):
            low, high = NORMAL_RANGES.get(key, (None, None))

            if low is None:
                continue

            if value < low:
                status = "low"
            elif value > high:
                status = "high"
            else:
                status = "normal"

            result[key] = {
                "value": value,
                "status": status,
                "severity": get_severity(value, low, high)
            }

    # -----------------------------
    # DISEASE CONDITIONS
    # -----------------------------
    DISEASE_CHECKS = {
        "typhoid": ["positive", "negative"],
        "malaria": ["positive", "negative"],
        "dengue": ["positive", "negative"],
        "covid": ["positive", "negative"],
        "hiv": ["positive", "negative"],
        "hbsag": ["positive", "negative"],
        "pregnancy": ["positive", "negative"],
    }

    for key, value in report_data.items():
        if isinstance(value, str):
            val = value.lower()

            for disease in DISEASE_CHECKS:
                if disease in key.lower():
                    if "positive" in val:
                        result[disease] = {
                            "value": value,
                            "status": "positive",
                            "severity": "high"
                        }
                    elif "negative" in val:
                        result[disease] = {
                            "value": value,
                            "status": "negative",
                            "severity": "normal"
                        }

    # -----------------------------
    # SPECIAL CONDITIONS
    # -----------------------------

    # Thyroid
    if "tsh" in report_data:
        tsh = report_data["tsh"]
        if tsh > 4:
            result["thyroid"] = {
                "status": "hypothyroidism",
                "severity": "moderate"
            }
        elif tsh < 0.4:
            result["thyroid"] = {
                "status": "hyperthyroidism",
                "severity": "moderate"
            }

    # Diabetes
    if "glucose" in report_data:
        glucose = report_data["glucose"]
        if glucose > 140:
            result["diabetes"] = {
                "status": "high risk",
                "severity": "high"
            }
        elif glucose > 100:
            result["diabetes"] = {
                "status": "prediabetes",
                "severity": "moderate"
            }

    # PCOD
    if "tsh" in report_data and "weight" in report_data:
        if report_data["tsh"] > 4:
            result["pcod_risk"] = {
                "status": "possible",
                "severity": "moderate"
            }

    # Anemia
    if "hemoglobin" in report_data:
        if report_data["hemoglobin"] < 12:
            result["anemia"] = {
                "status": "yes",
                "severity": "high"
            }

    # Liver
    if "bilirubin" in report_data:
        if report_data["bilirubin"] > 1.2:
            result["liver_issue"] = {
                "status": "possible",
                "severity": "moderate"
            }

    # Kidney
    if "creatinine" in report_data:
        if report_data["creatinine"] > 1.3:
            result["kidney_issue"] = {
                "status": "possible",
                "severity": "moderate"
            }

    # -----------------------------
    # SUMMARY
    # -----------------------------
    summary_list = []

    for key, val in result.items():
        if isinstance(val, dict):
            if val.get("status") in ["low", "high", "positive", "high risk"]:
                summary_list.append(f"{key} is {val.get('status')}")

    if not summary_list:
        result["summary"] = "All parameters are within normal range."
    else:
        result["summary"] = "Patient shows: " + ", ".join(summary_list)

    return result