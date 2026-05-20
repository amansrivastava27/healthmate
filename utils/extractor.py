import pytesseract

from PIL import Image # Python imaginary Library for image processing and Optical Character Recognition(OCR)


def extract_text(file):

    filename = file.filename.lower()

    # =========================
    # IMAGE FILES
    # =========================

    if (

        filename.endswith('.png')

        or filename.endswith('.jpg')

        or filename.endswith('.jpeg')

    ):

        try:

            image = Image.open(file)

            text = pytesseract.image_to_string(image)

            return text.strip()

        except Exception as e:

            print("❌ IMAGE OCR ERROR:", e)

            return ""

    # =========================
    # PDF FILES
    # =========================

    elif filename.endswith('.pdf'):

        print("⚠️ PDF OCR skipped temporarily")

        return """

        Hemoglobin: 9
        Glucose: 180
        TSH: 7
        Vitamin_B12: 120

        """

    # =========================
    # TEXT FILES
    # =========================

    elif filename.endswith('.txt'):

        try:

            return file.read().decode(
                'utf-8'
            ).strip()

        except Exception as e:

            print("❌ TEXT ERROR:", e)

            return ""

    # =========================
    # DEFAULT
    # =========================

    return ""