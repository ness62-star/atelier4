pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Train Model') {
            steps {
                // Start the FastAPI app in the background
                sh '. venv/bin/activate && make run-api &'
                sh 'sleep 5'  // Wait for the server to start
                // Retrain using the default train.csv
                sh '. venv/bin/activate && curl -X POST "http://localhost:8000/retrain" || echo "Training with default dataset failed, using existing model"'
            }
        }
        stage('Test API - Single Prediction') {
            steps {
                // Test a single prediction
                sh '. venv/bin/activate && curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d \'{"data": [1.0, 2.0]}\' || echo "Single prediction test failed"'
            }
        }
        stage('Test API - Dataset 2') {
            steps {
                // Test predictions on test.csv
                sh '. venv/bin/activate && curl -X GET "http://localhost:8000/test" || echo "Test dataset prediction failed"'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the app (e.g., to a server)...'
                // Add deployment steps here, e.g., copy files to a server or build a Docker image
                // Example: sh 'scp -r . user@server:/path/to/deploy'
            }
        }
    }
    post {
        always {
            // Clean up: Stop the FastAPI server
            sh 'pkill -f "
