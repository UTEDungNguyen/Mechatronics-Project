// Script Pipeline
node ('master')
{
    try 
    {
        stage('Delete All File in Jenkins Local')
        {   
            echo "Delete Folder in Jenkins Local"
            echo "================================"
            deleteDir()
            echo "Delete All File Successfully"
            echo "================================"
        }

        stage('Clone Newest Repository') 
        {
            echo "Starting Clone Repository"
            echo "================================"
            sh "git clone https://github.com/UTEDungNguyen/Mechatronics-Project.git"
            echo "Cloning Repository Successfully"
            echo "================================"
        }

        stage('Checking Repository is exist or not?') 
        {
            sh "ls"
        }

        stage('Get Path of Repo') 
        {
            sh 'pwd'
        }

        stage('Checkout to Branch running Jenkins File') 
        {
            dir('Mechatronics-Project') {
                sh 'pwd'
                echo "Starting Checkout Branch"
                echo "================================"
                sh "git checkout feature/jenkins-running-service"
                echo "Checkout Branch Successfully"
                echo "================================"
            }
        }

        stage('Check Current Branch') 
        {
            dir('Mechatronics-Project') {
                sh 'pwd'
                sh "git rev-parse --abbrev-ref HEAD" 
            }
        }

        stage('Check All File exist in Branch') 
        {
            dir('Mechatronics-Project')
            {
                sh 'pwd'
                sh "ls"
            }
        }

        stage('Execution Process Durian Classification') {
            dir('Mechatronics-Project') 
            {
                stage('DCMotor Executing')
                {
                    sh "python3 ControlDCMotor.py"
                }

                stage('Image Processing Executing')
                {
                    sh "python3 GetResultSample.py"
                }  

                stage('Capture Image Executing')
                {
                    sh "python3 CaptureRealTime.py"
                }
            }
        }
    }

    catch (Exception e) 
    {
        // Handle Error while running process and return error code
        echo "Build failed due to: ${e.message}"
        currentBuild.result = 'FAILURE'
    }

    finally
    {   
        // Run success
        if(currentBuild.result == 'SUCCESS')
        {
            echo "Running Jobs SUCCESS"
        }

        // Run Failed
        if(currentBuild.result == 'FAILURE')
        {
            echo "Running Jobs Failed"
        }

        // Connect Unstable
        if(currentBuild.result == 'UNSTABLE')
        {
            echo "Connect Unstable"
        }

        // Finish Jobs
        else 
        {
            echo "One way or another, Finished Running Jobs"
        }
    }
}