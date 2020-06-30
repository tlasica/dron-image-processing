pipeline {

    triggers {
        // Nightly means, there night somewhere around the world...
        // It's fine to let the job fire every fifteen minutes, as concurrent builds are not allowed.
        cron('H/15 * * * *')
    }

    agent { docker { image 'python:3.5.2' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}