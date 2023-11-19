include .env
export

.RECIPEPREFIX := $() $()

# ------------------------------------- PROD -------------------------------------------

COMPOSE_PROD :=                 \
    -f docker-compose.yaml      \
    -f ${COMPOSE_PROD_DB}       \
    -f ${COMPOSE_PROD_RABBIT}   \
    -f ${COMPOSE_PROD_REDIS}    \
    -f ${COMPOSE_PROD_WEB}      \

COMPOSE_PROD_ENV :=                             \
    --env-file=.env                             \
    --env-file=env/production/.env.prod.compose \

prodstart: docker-compose.yaml
    sudo docker compose -p prod ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} up --build --force-recreate

prodstop: docker-compose.yaml
    sudo docker compose -p prod ${COMPOSE_PROD_ENV} ${COMPOSE_PROD} down

# ------------------------------------- DEV -------------------------------------------

COMPOSE_DEV :=                  \
    -f docker-compose.yaml      \
    -f ${COMPOSE_DEV_DB}        \
    -f ${COMPOSE_DEV_RABBIT}    \
    -f ${COMPOSE_DEV_REDIS}     \
    -f ${COMPOSE_DEV_WEB}       \

COMPOSE_DEV_ENV :=                              \
    --env-file=.env                             \
    --env-file=env/development/.env.dev.compose \

devstart: docker-compose.yaml
    sudo docker compose -p dev ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} up --build --force-recreate

devstop: docker-compose.yaml
    sudo docker compose -p dev ${COMPOSE_DEV_ENV} ${COMPOSE_DEV} down

# ------------------------------------- TESTS -------------------------------------------

COMPOSE_TESTS :=                \
    -f docker-compose.yaml      \
    -f ${COMPOSE_TESTS_DB}      \
    -f ${COMPOSE_TESTS_RABBIT}  \
    -f ${COMPOSE_TESTS_REDIS}   \
    -f ${COMPOSE_TESTS_WEB}     \

COMPOSE_TESTS_ENV :=                        \
    --env-file=.env                         \
    --env-file=env/tests/.env.tests.compose \

GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m

itests: docker-compose.yaml
    sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} up -d --build
    @if [ `sudo docker wait tests-tests-1` -ne 0 ] ; then                                   \
        sudo docker logs tests-tests-1;                                                     \
        printf "${RED}Tests Failed${NC}\n";                                                 \
        sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} down;            \
    else                                                                                    \
        sudo docker logs tests-tests-1;                                                     \
        printf "${GREEN}Tests Passed${NC}\n";                                               \
        sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} down;            \
    fi                                                                                      \

# ------------------------------------- DOCS -------------------------------------------

docs:
    cd src/docs && make html

# ------------------------------------- K&8 -------------------------------------------

clusterstart:
    minikube start

clusterinit:
    kubectl create -f ${KA8_CLUSTER_PROD_NAMESPACE}
    kubectl wait --for jsonpath='{.status.phase}=Active' namespace/production --timeout=60s

    kubectl create -f ${KA8_CLUSTER_PROD_VOLUMES}
    while ! kubectl get pv pv-database-production-0 pv-database-production-1 pv-database-production-2 &> /dev/null; do \
    echo "Waiting for persistent volumes. CTRL-C to exit."; sleep 1; done                                              \

    kubectl create -f ${KA8_CLUSTER_PROD_ACCOUNT}
    while ! kubectl get serviceaccount service-account-production -n production &> /dev/null; do                       \
    echo "Waiting for service account. CTRL-C to exit."; sleep 1; done                                                 \

# create limit-range

# create quota

    kubectl create -f ${KA8_CLUSTER_PROD_SECRET_DJANGO}
    while ! kubectl get secret secret-django-production -n production &> /dev/null; do                                 \
    echo "Waiting for secret-django-production. CTRL-C to exit."; sleep 1; done                                        \

    kubectl create -f ${KA8_CLUSTER_PROD_SECRET_DB}
    while ! kubectl get secret secret-database-production -n production &> /dev/null; do                               \
    echo "Waiting for secret-database-production. CTRL-C to exit."; sleep 1; done                                      \

    kubectl create -f ${KA8_CLUSTER_PROD_SECRET_RABBIT}
    while ! kubectl get secret secret-rabbit-production -n production &> /dev/null; do                                 \
    echo "Waiting for secret-rabbit-production. CTRL-C to exit."; sleep 1; done                                        \

    kubectl create -f ${KA8_CLUSTER_PROD_SECRET_REDIS}
    while ! kubectl get secret secret-redis-production -n production &> /dev/null; do                                  \
    echo "Waiting for secret-redis-production. CTRL-C to exit."; sleep 1; done                                         \

    kubectl create secret generic certificate-https                                                                    \
    --from-file=certs/localhost-prod.crt --from-file=certs/localhost-prod.key -n production                            \

clusterrun:
    kubectl create -f ${KA8_CLUSTER_PROD_CONFIG}
    while ! kubectl get configmap configmap-django -n production &> /dev/null;              \
    do echo "Waiting for configmap-django. CTRL-C to exit."; sleep 1; done                  \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_DB_PUBLIC}
    while ! kubectl get service service-database-public -n production &> /dev/null; do      \
    echo "Waiting for service-database-public. CTRL-C to exit."; sleep 1; done              \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_DB_HEADLESS}
    while ! kubectl get service service-database-headless -n production &> /dev/null; do    \
    echo "Waiting for service-database-headless. CTRL-C to exit."; sleep 1; done            \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_RABBIT}
    while ! kubectl get service service-rabbitmq -n production &> /dev/null; do             \
    echo "Waiting for service-rabbitmq. CTRL-C to exit."; sleep 1; done                     \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_RABBIT_MANAGEMENT}
    while ! kubectl get service service-rabbitmq-management -n production &> /dev/null; do  \
    echo "Waiting for service-rabbitmq-management. CTRL-C to exit."; sleep 1; done          \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_REDIS}
    while ! kubectl get service service-redis -n production &> /dev/null; do                \
    echo "Waiting for service-redis. CTRL-C to exit."; sleep 1; done                        \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_SPHINX}
    while ! kubectl get service service-sphinx -n production &> /dev/null; do               \
    echo "Waiting for service-sphinx. CTRL-C to exit."; sleep 1; done                       \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_FLOWER}
    while ! kubectl get service service-flower -n production &> /dev/null; do               \
    echo "Waiting for service-flower. CTRL-C to exit."; sleep 1; done                       \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_GUNICORN}
    while ! kubectl get service service-gunicorn -n production &> /dev/null; do             \
    echo "Waiting for service-gunicorn. CTRL-C to exit."; sleep 1; done                     \

    kubectl create -f ${KA8_CLUSTER_PROD_SERVICE_NGINX}
    while ! kubectl get service service-nginx -n production &> /dev/null; do                \
    echo "Waiting for service-nginx. CTRL-C to exit."; sleep 1; done                        \

    kubectl create -f ${KA8_CLUSTER_PROD_STATEFULSET_DATABASE}
    kubectl rollout status statefulset statefulset-database -n production

    kubectl create -f ${KA8_CLUSTER_PROD_JOB_MIGRATIONS}
    kubectl wait --for=condition=complete job/job-migrations --timeout=-30s -n production

    chmod +x ${KA8_CLUSTER_PROD_DATABASE_REPLICATION_SCRIPT}
    ./${KA8_CLUSTER_PROD_DATABASE_REPLICATION_SCRIPT}

    kubectl create -f ${KA8_CLUSTER_PROD_DEPLOYMENT_RABBIT}
    kubectl rollout status deployment deployment-rabbitmq -n production

    kubectl create -f ${KA8_CLUSTER_PROD_DEPLOYMENT_REDIS}
    kubectl rollout status deployment deployment-redis -n production

    kubectl create -f ${KA8_CLUSTER_PROD_DEPLOYMENT_SPHINX}
    kubectl rollout status deployment deployment-sphinx -n production

    kubectl create -f ${KA8_CLUSTER_PROD_DEPLOYMENT_CELERY}
    kubectl rollout status deployment deployment-celery -n production

    kubectl create -f ${KA8_CLUSTER_PROD_DEPLOYMENT_GUNICORN}
    kubectl rollout status deployment deployment-gunicorn -n production

# nginx

    minikube addons enable metrics-server
    kubectl rollout status deployment metrics-server -n kube-system
    while ! kubectl top pod --all-namespaces &> /dev/null; do                               \
    echo "Waiting for collecting metrics. CTRL-C to exit."; sleep 1; done                   \

# hpas

clusterpause:
    minikube pause

clusterresume:
    minikube unpause

clusterclear:
    kubectl delete namespace production
    kubectl delete pv pv-database-production-0 pv-database-production-1 pv-database-production-2

clusterstop:
    minikube stop

clusterdelete:
    minikube delete