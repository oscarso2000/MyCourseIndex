docker build -t cs4300piazza .
docker tag cs4300piazza mb2363/cs4300piazza:latest
docker tag cs4300piazza mb2363/cs4300piazza:$TRAVIS_BUILD_NUMBER
docker push mb2363/cs4300piazza:latest
docker push mb2363/cs4300piazza:$TRAVIS_BUILD_NUMBER