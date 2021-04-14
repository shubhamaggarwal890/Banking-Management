pipeline {
    agent any
    environment {
        imageName = ""
    }
    stages {
        stage('Testing') {
            steps {
                sh 'python3 admin_tests.py'
            }
        }
        stage('Containerization') {
           steps {
               script {
                   imageName = docker.build "shubhamaggarwal890/banking-management:latest"
               }
           }
        }
        stage('Push Docker Image') {
            steps {
                script{
                    docker.withRegistry('', 'docker-credentials') {
                        imageName.push()
                    }
                }
            }
        }
    }
}
