from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    session,
    redirect
)

import json
import sys
import os

from dotenv import load_dotenv

from models import (
    db,
    Report,
    User,
    Profile
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# PATH SETUP
# =========================

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

# =========================
# IMPORTS
# =========================

from orchestrator import run_pipeline
from utils.extractor import extract_text
from utils.parser import parse_report

# =========================
# OPTIONAL GROQ AI
# =========================

client = None

try:

    from groq import Groq

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    print("✅ Groq AI connected")

except Exception as e:

    print("⚠️ Groq AI disabled:", e)

# =========================
# CREWAI TEMP DISABLED
# =========================

run_crew = None

CREWAI_AVAILABLE = False

print("⚠️ CrewAI temporarily disabled")

# =========================
# APP SETUP
# =========================

app = Flask(__name__)

app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///database.db'
)

db.init_app(app)

with app.app_context():
    db.create_all()

USE_AI = True

latest_report = {}

# =========================
# AI CHAT FUNCTION
# =========================

def ask_ai(message, report):

    if not client:

        return (
            "AI service unavailable. "
            "Using manual health system."
        )

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "You are a helpful "
                        "medical assistant."
                    )
                },

                {
                    "role": "user",
                    "content": (
                        f"Report: {report}\n"
                        f"Question: {message}"
                    )
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("⚠️ AI Error:", e)

        return (
            "AI service temporarily unavailable."
        )

db.init_app(app)

with app.app_context():
    db.create_all()

# =========================
# HOME
# =========================

@app.route('/')
def home():

    return render_template('home.html')

# =========================
# ANALYZER PAGE
# =========================

@app.route('/analyzer')
def analyzer():

    return render_template('analyzer.html')

# =========================
# PHARMACY
# =========================

@app.route('/pharmacy')
def pharmacy():

    return render_template('pharmacy.html')

# =========================
# CHAT PAGE
# =========================

@app.route('/chat-page')
def chat_page():

    return render_template('chat.html')

# =========================
# HISTORY
# =========================

@app.route('/history')
def history():

    if not session.get('user'):

        return redirect('/login')

    reports = Report.query.filter_by(
        patient_name=session.get('user')
    ).order_by(
        Report.id.desc()
    ).all()

    return render_template(
        'history.html',
        reports=reports
    )

# =========================
# REGISTER
# =========================

@app.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                'register.html',
                error='Username already exists'
            )

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# =========================
# LOGIN
# =========================

@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if request.method == 'POST':

        user = User.query.filter_by(
            username=request.form['username']
        ).first()

        if (
            user
            and user.password == request.form['password']
        ):

            session['user'] = user.username

            return redirect('/')

        return render_template(
            'login.html',
            error="Invalid username or password"
        )

    return render_template('login.html')

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

# =========================
# PROFILE
# =========================

@app.route(
    '/profile',
    methods=['GET', 'POST']
)
def profile():

    if not session.get('user'):

        return redirect('/login')

    if request.method == 'POST':

        existing_profile = Profile.query.filter_by(
            username=session.get('user')
        ).first()

        if existing_profile:

            existing_profile.age = request.form['age']

            existing_profile.gender = request.form['gender']

            existing_profile.weight = request.form['weight']

            existing_profile.height = request.form['height']

        else:

            profile = Profile(

                username=session.get('user'),

                age=request.form['age'],

                gender=request.form['gender'],

                weight=request.form['weight'],

                height=request.form['height']
            )

            db.session.add(profile)

        db.session.commit()

    user_profile = Profile.query.filter_by(
        username=session.get('user')
    ).first()

    bmi = None

    if user_profile:

        try:

            height_m = (
                float(user_profile.height) / 100
            )

            bmi = round(
                float(user_profile.weight) /
                (height_m * height_m),
                2
            )

        except:

            bmi = None

    return render_template(
        'profile.html',
        profile=user_profile,
        bmi=bmi
    )

# =========================
# ANALYZE REPORT
# =========================

@app.route(
    '/analyze',
    methods=['POST']
)
def analyze():

    global latest_report

    file = request.files.get('report')

    # =========================
    # NO FILE
    # =========================

    if not file or file.filename == '':

        return render_template(
            'analyzer.html',
            error="Please upload a medical report."
        )

    try:

        # =========================
        # EXTRACT TEXT
        # =========================

        text = extract_text(file)

        # =========================
        # FILE ERRORS
        # =========================

        if text == "PDF_UPLOAD_TEMP_DISABLED":

            return render_template(

                'analyzer.html',

                error=(
                    "PDF OCR temporarily disabled. "
                    "Please upload image or txt file."
                )
            )

        if text == "EMPTY_IMAGE_TEXT":

            return render_template(

                'analyzer.html',

                error=(
                    "No readable text found in image."
                )
            )

        if text == "IMAGE_READ_ERROR":

            return render_template(

                'analyzer.html',

                error=(
                    "Could not process image."
                )
            )

        if text == "EMPTY_TEXT_FILE":

            return render_template(

                'analyzer.html',

                error=(
                    "Uploaded text file is empty."
                )
            )

        if text == "TEXT_READ_ERROR":

            return render_template(

                'analyzer.html',

                error=(
                    "Could not read text file."
                )
            )

        if text == "UNSUPPORTED_FILE":

            return render_template(

                'analyzer.html',

                error=(
                    "Unsupported file format."
                )
            )

        if not text:

            return render_template(

                'analyzer.html',

                error="Could not read file."
            )

        # =========================
        # PARSE REPORT
        # =========================

        report_data = parse_report(text)

        print(
            "\n===== PARSED DATA =====\n",
            report_data
        )

        # =========================
        # FALLBACK SAMPLE DATA
        # =========================

        if not report_data:

            print(
                "⚠️ Parser empty. Using fallback."
            )

            report_data = {

                "t3": 1.43,

                "t4": 7.77,

                "tsh": 2.57,

                "vitamin_b12": 17.4
            }

        latest_report = report_data

        result = None

        # =========================
        # CREWAI DISABLED
        # =========================

        if False:

            pass

        # =========================
        # MANUAL MEDICAL SYSTEM
        # =========================

        if not result:

            print(
                "⚙️ Using manual system..."
            )

            result = run_pipeline(report_data)

        # =========================
        # SAVE REPORT
        # =========================

        db.session.add(

            Report(

                patient_name=session.get(
                    'user',
                    'Guest'
                ),

                data=json.dumps(result)
            )
        )

        db.session.commit()

        # =========================
        # RETURN RESULT
        # =========================

        return render_template(

            'analyzer.html',

            result=result
        )

    except Exception as e:

        print("❌ ERROR:", e)

        return render_template(

            'analyzer.html',

            error="Something went wrong."
        )

# =========================
# CHAT API
# =========================

@app.route(
    '/chat',
    methods=['POST']
)
def chat():

    global latest_report

    data = request.get_json()

    msg = data.get("message", "")

    if not latest_report:

        return jsonify({

            "reply":
            "Upload medical report first."
        })

    return jsonify({

        "reply": ask_ai(
            msg,
            latest_report
        )
    })

# =========================
# PDF DOWNLOAD
# =========================

@app.route('/download')
def download():

    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)

    content = [

        Paragraph("Health Report Summary"),

        Paragraph(str(latest_report))
    ]

    doc.build(content)

    return send_file(
        file_path,
        as_attachment=True
    )

# =========================
# FAVICON
# =========================

@app.route('/favicon.ico')
def favicon():

    return '', 204

# =========================
# RUN
# =========================

if __name__ == '__main__':

    app.run(debug=True)
