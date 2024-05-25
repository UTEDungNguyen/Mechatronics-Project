// Script Pipeline
node
{                   
    try 
    {
        dir('/home/pi/jenkins_home/workspace/Mechatronics_Jenkins')
        {
            stage('Check Process of Python3 Execution')
            {   
                echo "Check process of Python3"
                echo "================================"
                sh "ps aux | grep python3"
            }

            stage('Kill All Process Define')
            {
                stage('Kill Control DC Motor Process')
                {
                    echo "Kill Control DCMotor Process"
                    sh "sudo pkill -f ControlDCMotor.py"
                }

                stage('Kill Get Result of Durian Process')
                {
                    echo "Kill Get Result Process"
                    sh "sudo pkill -f GetResultSample.py"
                }

                stage('Kill Capture Image Process')
                {
                    echo "Kill CApture Image Process"
                    sh "sudo pkill -f CaptureRealTime.py"
                }
            }

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

            stage('Execution Process Durian Classification') 
            {
                dir('Mechatronics-Project') 
                {
                    stage('DCMotor Executing')
                    {
                        sh "nohup sudo python3 ControlDCMotor.py &"
                        // sh "sudo python3 ControlDCMotor.py"
                    }

                    stage('Image Processing Executing')
                    {
                        sh "nohup sudo python3 GetResultSample.py &"
                        // sh 'pip3 install qrcode'
                        // sh 'pip3 install pyrebase'
                        // sh "python3 GetResultSample.py"
                    }  

                    stage('Capture Image Executing')
                    {
                        sh "nohup sudo python3 CaptureRealTime.py &"
                        // sh "python3 CaptureRealTime.py"
                    }
                }
            }

            // Send success email
            emailext (
                subject: "Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Success",
                body: """
                    <p><strong>Good news Developer,</strong></p>
                    <p>The job <strong>'${env.JOB_NAME}'</strong> completed successfully.</p>
                    <p>Check the build details <a href='${env.BUILD_URL}'>here</a>.</p>
                    <p>The durian classify machine is ready to run.</p>
                    <p>Have a nice day!!!</strong></p>

                    <p>Sincerely,</p>
                    <p>--------------------------------------------------------</p>
                    <p><strong>Jenkins Service</strong></p>
                    <p><strong>Ho Chi Minh University of Technology and Education</strong></p>
                    <p><strong>Expertise : Mechatronics</strong></p>
                    <p><strong>Email : dungduide2002@gmail.com</strong></p>
                    <p><strong>Telephone : 0785180902</strong></p>
                """,
                to: 'dungduide2002@gmail.com',
                mimeType: 'text/html'
            )
        }
    }

    catch (Exception e) 
    {
        // Handle Error while running process and return error code
        echo "Build failed due to: ${e.message}"
        currentBuild.result = 'FAILURE'

        // Send failed email
        emailext (
            subject: "Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Failure",
            body: """
                <p><strong>Dear Developer,</strong></p>
                <p>The job '<strong>${env.JOB_NAME}</strong>' has failed.</p>
                <p>Error: <strong>${e}.</strong></p>
                <p>Check the build details <a href='${env.BUILD_URL}'>here</a>.</p>
                <p>The durian classify machine is not ready to run.</p>
                <p>Have a nice day!!!</strong></p>

                <p>Sincerely,</p>
                <p>--------------------------------------------------------</p>
                <p><strong>Jenkins Service</strong></p>
                <p><strong>Ho Chi Minh University of Technology and Education</strong></p>
                <p><strong>Expertise : Mechatronics</strong></p>
                <p><strong>Email : dungduide2002@gmail.com</strong></p>
                <p><strong>Telephone : 0785180902</strong></p>
            """,
            to: 'dungduide2002@gmail.com',
            mimeType: 'text/html'
        )
        // Throw exception
        throw e
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