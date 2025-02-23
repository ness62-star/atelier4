pipeline {
    agent any
    environment {
        VENV = "venv"
        PYTHON = "python"
    }
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    echo "Cloning the latest code from GitHub..."
                    checkout scm
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo "Creating and activating virtual environment..."
                    bat '''
                        if not exist venv python -m venv venv
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "Installing dependencies..."
                    bat '''
                        call venv\\Scripts\\activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run FastAPI') {
            steps {
                script {
                    echo "Starting FastAPI server..."
                    bat '''
                        call venv\\Scripts\\activate
                        uvicorn app:app --host 0.0.0.0 --port 8000
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            bat '''
                call venv\\Scripts\\deactivate.bat
            '''
        }
    }
}
