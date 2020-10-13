branch="$TRAVIS_BRANCH" #$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')

if ["$branch" = "master"]
then
    docker build -t cs4300piazza .
    docker tag cs4300piazza oscarso2000/cs4300piazza:latest
    docker tag cs4300piazza oscarso2000/cs4300piazza:$TRAVIS_BUILD_NUMBER
    docker push oscarso2000/cs4300piazza:latest
    docker push oscarso2000/cs4300piazza:$TRAVIS_BUILD_NUMBER

    docker build -t cs4300docs -f docs/Dockerfile .
    docker tag cs4300docs oscarso2000/cs4300docs:latest
    docker tag cs4300docs oscarso2000/cs4300docs:$TRAVIS_BUILD_NUMBER
    docker push oscarso2000/cs4300docs:latest
    docker push oscarso2000/cs4300docs:$TRAVIS_BUILD_NUMBER
elif ["$branch" = "dev"]
then
    docker build -t mciDev .
    docker tag mciDev oscarso2000/mciDev:latest
    docker tag mciDev oscarso2000/mciDev:$TRAVIS_BUILD_NUMBER
    docker push oscarso2000/mciDev:latest
    docker push oscarso2000/mciDev:$TRAVIS_BUILD_NUMBER
else
    docker build -t mciTest .
fi

echo 'Successfully built'
