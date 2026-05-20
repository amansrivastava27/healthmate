import re

def safe_float(val):
    try:
        return float(val)
    except:
        return None


def parse_report(text):
    data = {}

    try:
        # Normalize text
        text = text.replace(",", " ")
        text = re.sub(r"\s+", " ", text)

        # -------------------------
        # T3
        # -------------------------
        t3 = re.search(r"(T3|Serum T3)[^\d]*([\d]+\.?\d*)", text, re.IGNORECASE)
        if t3:
            val = safe_float(t3.group(2))
            if val:
                data["t3"] = val

        # -------------------------
        # T4
        # -------------------------
        t4 = re.search(r"(T4|Serum T4)[^\d]*([\d]+\.?\d*)", text, re.IGNORECASE)
        if t4:
            val = safe_float(t4.group(2))
            if val:
                data["t4"] = val

        # -------------------------
        # TSH
        # -------------------------
        tsh = re.search(r"(TSH|Serum TSH)[^\d]*([\d]+\.?\d*)", text, re.IGNORECASE)

        if tsh:
            val = safe_float(tsh.group(2))
            if val:
                data["tsh"] = val

        # -------------------------
        # Vitamin B12
        # -------------------------


        b12 = re.search(
                r"(Vitamin\s*B12|VB\s*12|Active Vitamin B12)[^\d]*([\d]+\.?\d*)", 
                text,re.IGNORECASE
                )

        if b12:
            val = safe_float(b12.group(2))
            if val:
                data["vitamin_b12"] = val

    except Exception as e:

        print("Parser error:", e)
    return data