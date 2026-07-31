from flask import Flask, request, render_template_string
import os
import re
from collections import Counter
import math

app = Flask(__name__)

# Read values from Kubernetes ConfigMap (or use defaults)
APP_TITLE = os.getenv("APP_TITLE", "Local ATS Match Checker")
APP_SUBTITLE = os.getenv("APP_SUBTITLE", "Local ATS Score Checker")

# Simple Text Similarity Algorithm (Cosine Similarity)
def get_ats_score(text1, text2):
    WORD = re.compile(r'\w+')

    def text_to_vector(text):
        words = WORD.findall(text.lower())
        return Counter(words)

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum([vector1[x] * vector2[x] for x in intersection])

    sum1 = sum([vector1[x] ** 2 for x in vector1.keys()])
    sum2 = sum([vector2[x] ** 2 for x in vector2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return round((float(numerator) / denominator) * 100, 2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #1e1e2e;
            color: #cdd6f4;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: #313244;
            padding: 30px;
            border-radius: 8px;
        }

        textarea {
            width: 100%;
            height: 150px;
            background: #45475a;
            color: #fff;
            border: 1px solid #585b70;
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 20px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            background-color: #a6e3a1;
            color: #11111b;
            border: none;
            padding: 12px 20px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            background: #11111b;
            border-left: 5px solid #89b4fa;
            border-radius: 4px;
        }

        h1 {
            color: #89b4fa;
        }
    </style>
</head>

<body>

<div class="container">

<h1>🔍 {{ app_title }}</h1>

<form method="POST">

<label><h3>1. Paste Job Description:</h3></label>

<textarea
name="job_desc"
placeholder="Paste the target job requirements here..."
required></textarea>

<label><h3>2. Paste Resume Text:</h3></label>

<textarea
name="resume"
placeholder="Paste the candidate resume content here..."
required></textarea>

<input type="submit" value="Calculate ATS Score">

</form>

{% if score is not none %}

<div class="result">

<h2>
📈 ATS Match Rating:
<span style="color:#a6e3a1;">{{ score }}%</span>
</h2>

<p>
Your resume matches the vocabulary profile of this job description by {{ score }}%.
</p>

</div>

{% endif %}

</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    score = None

    if request.method == 'POST':
        job_desc = request.form.get('job_desc', '')
        resume = request.form.get('resume', '')

        score = get_ats_score(job_desc, resume)

        with open("/data/ats_logs.txt", "a") as f:
            f.write(f"ATS Score: {score}%\n")

    return render_template_string(
        HTML_TEMPLATE,
        score=score,
        app_title=APP_TITLE,
        app_subtitle=APP_SUBTITLE
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
