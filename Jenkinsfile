pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }
        stage('Start FastAPI Server') {
            steps {
                echo 'Starting FastAPI server in the background...'
                bat 'start /B venv\\Scripts\\uvicorn app:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1'
                // Use ping to wait 10 seconds (pinging localhost 10 times, ~1 sec each)
                bat 'ping 127.0.0.1 -n 11 > nul'  // -n 11 gives ~10 seconds delay
            }
        }
        stage('Train Model with train.csv') {
            steps {
                echo 'Retraining model with train.csv...'
                bat 'venv\\Scripts\\activate && curl -X POST "http://localhost:8000/retrain" || echo Retraining failed, proceeding with existing model'
                bat 'ping 127.0.0.1 -n 6 > nul'  // Wait ~5 seconds
            }
        }
        stage('Test Single Prediction') {
            steps {
                echo 'Testing single prediction...'
                bat 'venv\\Scripts\\activate && curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\\"data\\": [1.0, 2.0]}" || echo Single prediction test failed'
            }
        }
        stage('Test Dataset 2 (test.csv)') {
            steps {
                echo 'Testing predictions on test.csv...'
                bat 'venv\\Scripts\\activate && curl -X GET "http://localhost:8000/test" || echo Test dataset prediction failed'
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            bat 'taskkill /F /IM uvicorn.exe /T || echo No Uvicorn process found'
            archiveArtifacts artifacts: 'fastapi.log', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs in fastapi.log.'
        }
    }
}
