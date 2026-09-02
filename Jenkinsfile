pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        ansiColor('xterm')
    }

    environment {
        PYTHON_VERSION = '3.11'
        REGISTRY = 'ghcr.io/donny-devops/pipefish-labs'
        IMAGE_NAME = 'mcp-server'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Codebase') {
            steps {
                checkout scm
                sh 'git log -1 --stat'
            }
        }

        stage('Set Up Environment') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -e ".[dev]"
                '''
            }
        }

        stage('Code Linting & Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s tests -p "test_*.py"
                '''
            }
        }

        stage('DOM & Media Integrity Verification') {
            steps {
                sh '''
                    . venv/bin/activate
                    python scripts/verify_dom_integrity.py
                '''
            }
        }

        stage('API Contract Verification (Newman)') {
            steps {
                sh '''
                    if command -v newman >/dev/null 2>&1; then
                        newman run postman/pipefish_collection.json -e postman/pipefish_environment.json --reporters cli,junit --reporter-junit-export newman-results.xml
                    else
                        echo "Newman not installed on agent. Skipping live Newman execution."
                    fi
                '''
            }
        }

        stage('Build Hardened Docker Container') {
            steps {
                sh '''
                    docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} -t ${REGISTRY}/${IMAGE_NAME}:latest -f Dockerfile.mcp .
                '''
            }
        }

        stage('Container Security Scan (Trivy)') {
            steps {
                sh '''
                    if command -v trivy >/dev/null 2>&1; then
                        trivy image --severity HIGH,CRITICAL ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    else
                        echo "Trivy not installed on agent. Skipping container scan."
                    fi
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "Pipeline succeeded! PipeFish Labs multi-agent artifacts verified."
        }
        failure {
            echo "Pipeline failed. Check build logs."
        }
    }
}
