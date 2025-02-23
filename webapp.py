from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "http://localhost:8000"  # FastAPI server URL

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    test_predictions = None
    retrain_message = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "predict":
            try:
                data = [float(x) for x in request.form.get("data").split(",")]
                response = requests.post(f"{API_URL}/predict", json={"data": data})
                prediction = response.json()["prediction"] if response.ok else f"Error: {response.text}"
            except Exception as e:
                prediction = f"Invalid input: {str(e)}"

        elif action == "test":
            try:
                response = requests.get(f"{API_URL}/test")
                test_predictions = response.json()["predictions"] if response.ok else f"Error: {response.text}"
            except Exception as e:
                test_predictions = f"Error: {str(e)}"

        elif action == "retrain":
            try:
                if "use_default" in request.form:
                    response = requests.post(f"{API_URL}/retrain")
                else:
                    data = [[float(x) for x in row.split(",")] for row in request.form.get("retrain_data").split(";")]
                    labels = [int(x) for x in request.form.get("labels").split(",")]
                    hyperparams = {
                        "max_depth": int(request.form.get("max_depth", 5)),
                        "min_samples_split": int(request.form.get("min_samples_split", 2))
                    }
                    response = requests.post(f"{API_URL}/retrain", json={"data": data, "labels": labels, "hyperparams": hyperparams})
                retrain_message = response.json()["message"] if response.ok else f"Error: {response.text}"
            except Exception as e:
                retrain_message = f"Invalid input: {str(e)}"

    return render_template("index.html", prediction=prediction, test_predictions=test_predictions, retrain_message=retrain_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
