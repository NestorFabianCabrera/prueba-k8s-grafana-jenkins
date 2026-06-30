pipeline {
    agent any

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'staging', 'prod'], description: 'Entorno de destino')
    }

    environment {
        IMAGE_NAME = 'danieldaza14/app'
        IMAGE_TAG  = '1.0'
        KUBE_NS    = 'mi-namespace'
        REGISTRY_CREDENTIALS = credentials('registry-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG ./app'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run -d --rm --name app-test $IMAGE_NAME:$IMAGE_TAG
                    APP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' app-test)
                    for i in $(seq 1 10); do
                      if curl -fsS http://$APP_IP:8080/health; then
                        break
                      fi
                      sleep 2
                    done
                    curl -fsS http://$APP_IP:8080/health
                    docker stop app-test
                '''
            }
        }

        stage('Push') {
            steps {
                sh '''
                    echo "$REGISTRY_CREDENTIALS_PSW" | docker login -u "$REGISTRY_CREDENTIALS_USR" --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh "kubectl apply -n ${KUBE_NS} -f k8s/namespace.yaml -f k8s/configmap.yaml -f k8s/secret.yaml -f k8s/deploy.yaml -f k8s/service.yaml -f k8s/ingress.yaml -f k8s/daemonset.yaml -f k8s/pdb.yaml -f k8s/hpa.yaml"
            }
        }

        stage('Smoke test') {
            steps {
                script {
                    try {
                        sh "kubectl rollout status deployment/app -n ${KUBE_NS} --timeout=120s"
                    } catch (err) {
                        sh "kubectl rollout undo deployment/app -n ${KUBE_NS}"
                        error "Smoke test failed, rollback ejecutado: ${err}"
                    }
                }
            }
        }

        stage('Notify') {
            steps {
                echo "Deployment successful on ${params.TARGET_ENV}"
            }
        }
    }
}
