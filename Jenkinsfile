pipeline{
    agent any
    
    environment {
	IMAGE_NAME: 'daniel'
	IMAGE_TAG: '1.0'
	KUBE_NS: 'mi-namespace'
	TARGET_ENV: 'dev'
    }
    stages{
        stage(checkout){
            steps {
                git clone 'https://github.com/prueba-k8s-grafana-jenkins'
                sh 'git checkout main'
                sh 'git pull'
                sh 'git status'
                sh 'git log'
            }
        }
        stage(build){
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }
        stage(test){
            steps {
                sh 'docker run --rm $IMAGE_NAME:$IMAGE_TAG test'
            }
        }
        stage(push){
            steps {
                sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
            }
        }
	stage(deploy){
	    steps{
                sh 'kubectl apply -f   k8s/deployment.yaml'
	    }
	}
	stage(smoke test){
	    steps{
                sh 'kubectl rollout status deployment/$IMAGE_NAME'
	    }
	}
	stage(notify){
	    steps{
                sh 'echo "Deployment successful"'
	    }
        }
   }
}
