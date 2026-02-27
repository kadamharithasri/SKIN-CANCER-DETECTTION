from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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

    if len(files) < 1:
        return render_template('dashboard.html',
                               error="Please upload images.")

    results = []
    image_paths = []

    melanoma_count = 0
    non_melanoma_count = 0
    no_cancer_count = 0

    for file in files:

        if file.filename == '':
            continue

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Dummy Prediction
        prediction = random.choice([
            "Melanoma",
            "Non-Melanoma",
            "No Cancer Detected"
        ])

        if prediction == "Melanoma":
            melanoma_count += 1
        elif prediction == "Non-Melanoma":
            non_melanoma_count += 1
        else:
            no_cancer_count += 1

        results.append(prediction)
        image_paths.append(filepath)

    total_images = len(results)

    return render_template(
        'dashboard.html',
        results=results,
        image_paths=image_paths,
        total_images=total_images,
        melanoma_count=melanoma_count,
        non_melanoma_count=non_melanoma_count,
        no_cancer_count=no_cancer_count
    )

if __name__ == '__main__':
    app.run(debug=True)