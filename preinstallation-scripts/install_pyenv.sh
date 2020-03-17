if [ "$(uname)" == "Darwin" ]; then
    # Do something under Mac OS X platform
    /usr/local/bin/brew update
    /usr/local/bin/brew install pyenv
    pyenv install 3.6.10
    pyenv install 3.7.6
    pyenv install 3.8.1
    pyenv global 3.6.10      
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Do something under GNU/Linux platform
    sudo apt-get update
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    curl https://pyenv.run | bash
    echo 'export PATH="/home/ubuntu/.pyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    source ~/.bashrc
    pyenv install 3.6.8
    pyenv install 3.7.6
    pyenv install 3.8.1
    pyenv global 3.7.6
else
    # Not Unix System
    echo "Sorry, we currently don't handle this OS."
fi
