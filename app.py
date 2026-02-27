from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login():
    return render_template('login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ---------------- PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():

    files = request.files.getlist("images")

    if len(files) == 0:
        return render_template('dashboard.html',
                               error="Please upload images.")

    results = []

    melanoma_count = 0
    non_melanoma_count = 0
    no_cancer_count = 0

    for file in files:

        if file.filename == '':
            continue

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Dummy Prediction (Replace with ML model later)
        prediction = random.choice([
            "Melanoma",
            "Non-Melanoma",
            "No Cancer Detected"
        ])

        confidence = round(random.uniform(80, 99), 2)

        if prediction == "Melanoma":
            melanoma_count += 1
            color = "red"
        elif prediction == "Non-Melanoma":
            non_melanoma_count += 1
            color = "orange"
        else:
            no_cancer_count += 1
            color = "green"

        results.append({
            "filename": filename,
            "filepath": filepath,
            "prediction": prediction,
            "confidence": confidence,
            "color": color
        })

    total_images = len(results)

    return render_template(
        'dashboard.html',
        results=results,
        total_images=total_images,
        melanoma_count=melanoma_count,
        non_melanoma_count=non_melanoma_count,
        no_cancer_count=no_cancer_count
    )

if __name__ == '__main__':
    app.run(debug=True)