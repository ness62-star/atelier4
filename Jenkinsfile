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
                        pip install --default-timeout=1000  --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
                    '''
                }
            }
        }

        stage('List Files') {
            steps {
                script {
                    echo "Listing files in workspace..."
                    bat 'dir'  // For Windows
                }
            }
        }

        stage('Copy Model') {
            steps {
                script {
                    echo "Copying model to workspace..."
                    bat 'copy decision_tree_model.pkl .'
                    sh 'cp decision_tree_model.pkl .'
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
