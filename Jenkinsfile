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
            // emailext (
            //     subject: "Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Success",
            //     body: """
            //         <p>Good news,</p>
            //         <p>The job '${env.JOB_NAME}' completed successfully.</p>
            //         <p>Check the build details <a href='${env.BUILD_URL}'>here</a>.</p>
            //     """,
            //     recipientProviders: [[$class: 'DevelopersRecipientProvider']],
            //     mimeType: 'text/html'
            // )
        }
        mail bcc: '', body: '''         <p>Good news,</p>
           <p>The job completed successfully.</p>
            <p>Check the build details here</a>.</p>''', 
            cc: '', 
            from: '', 
            replyTo: '', 
            subject: 'Jenkins Service Build Project Status', 
            to: 'dungduide2002@gmail.com'

    }

    catch (Exception e) 
    {
        // Handle Error while running process and return error code
        echo "Build failed due to: ${e.message}"
        currentBuild.result = 'FAILURE'
        // // Send failure email
        // emailext (
        //     subject: "Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL}) Failure",
        //     body: """
        //         <p>Dear Developer,</p>
        //         <p>The job '${env.JOB_NAME}' has failed.</p>
        //         <p>Error: ${e}</p>
        //         <p>Check the build details <a href='${env.BUILD_URL}'>here</a>.</p>
        //     """,
        //     recipientProviders: [[$class: 'DevelopersRecipientProvider']],
        //     mimeType: 'text/html'
        // )
        // // Re-throw the exception to mark the build as failed
        // throw e
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