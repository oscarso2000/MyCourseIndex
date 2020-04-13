docker build -t cs4300piazza .
docker tag cs4300piazza oscarso2000/cs4300piazza:latest
docker tag cs4300piazza oscarso2000/cs4300piazza:$TRAVIS_BUILD_NUMBER
docker push oscarso2000/cs4300piazza:latest
docker push oscarso2000/cs4300piazza:$TRAVIS_BUILD_NUMBER