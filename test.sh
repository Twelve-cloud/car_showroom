RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
cleanup () {
	sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} down
}
trap 'cleanup ; printf "${RED}Tests Failed For Unexpected Reasons${NC}\n"' HUP INT QUIT PIPE TERM
sudo docker compose -p tests ${COMPOSE_TESTS_ENV} ${COMPOSE_TESTS} up -d --build
if [ $? -ne 0 ] ; then
	printf "${RED}Docker Compose Failed${NC}\n"
	exit -1
fi
TEST_EXIT_CODE=`docker wait tests-tests-1`
docker logs tests-tests-1
if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
	printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
	printf "${GREEN}Tests Passed${NC}\n"
fi
cleanup
exit $TEST_EXIT_CODE