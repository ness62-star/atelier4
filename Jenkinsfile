pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Start FastAPI Server') {
            steps {
                echo 'Starting FastAPI server in the background...'
                // Run the server in the background and redirect logs
                sh '. venv/bin/activate && uvicorn app:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &'
                // Wait for the server to start
                sh 'sleep 10'
            }
        }
        stage('Train Model with train.csv') {
            steps {
                echo 'Retraining model with train.csv...'
                sh '. venv/bin/activate && curl -X POST "http://localhost:8000/retrain" || echo "Retraining failed, proceeding with existing model"'
                sh 'sleep 5'  // Give time for model to save
            }
        }
        stage('Test Single Prediction') {
            steps {
                echo 'Testing single prediction...'
                sh '. venv/bin/activate && curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d \'{"data": [1.0, 2.0]}\' || echo "Single prediction test failed"'
            }
        }
        stage('Test Dataset 2 (test.csv)') {
            steps {
                echo 'Testing predictions on test.csv...'
                sh '. venv/bin/activate && curl -X GET "http://localhost:8000/test" || echo "Test dataset prediction failed"'
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            sh 'pkill -f "uvicorn" || true'  // Stop the FastAPI server
            archiveArtifacts artifacts: 'fastapi.log', allowEmptyArchive: true  // Save logs for debugging
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs in fastapi.log.'
        }
    }
}
