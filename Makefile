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
        exit 1;                                                                             \
    else                                                                                    \
        sudo docker logs tests-tests-1;                                                     \
        printf "${GREEN}Tests Passed${NC}\n";                                               \
    fi                                                                                      \

stop:
    sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} down;            \
# ------------------------------------- DOCS -------------------------------------------

docs:
    cd src/docs && make html
