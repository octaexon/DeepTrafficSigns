### Links
[home](../README.md) &#8226; [intro](introduction.md) &#8226; [env](environment.md)



### Environment

Before launching into the nitty gritty, I should spare a word or two for my development environment.
I'm working on that renowned workhorse of high performance computing, the MacBook Air. Indeed, we'll
talk about the cloud later, but for the moment:

- **shell** I use the zsh (it waiting for you in /bin) with the
  [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) framework for configuration. What is
  especially nice is the host of plugins that oh-my-zsh provides.  Honestly, I don't think I'll ever
  go back to bash.

- **packaging** [Homebrew](https://brew.sh) is my package manager of choice.

- **python** [pyenv](https://github.com/pyenv/pyenv) and
  [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) are simply fantastic.  During the
  development of this project, there was a fragility in running the [Tensorflow Object
  Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) on
  the Google Cloud Platform ML Engine using the python 3.5 runtime, meaning to say that it simply
  didn't work in the cloud.  The other option provided in
  the cloud is the python 2.7 runtime.

  So I wanted to be able to switch between python 3.5 and 2.7 effortlessly, while still maintaining
  the insulation of their respective virtual environments.  The pyenv/pyenv-virtualenv combination
  makes this a doddle.  To install:
  ```zsh
  brew install pyenv pyenv-virtualenv
  ```
  Actually, with oh-my-zsh their configuration is completed just by enabling the pyenv plugin in
  your .zshrc file. (Awesome).  Let's install the two python versions in which we are interested:
  ```zsh
  pyenv install 3.5.0 2.7.9
  ```
  Create two named virtual environments:
  ```zsh
  pyenv virtualenv 3.5.0 dts3
  pyenv virtualenv 2.7.9 dts2
  ```
  We can now attach them to our project:
  ```zsh
  # within root directory of our project
  pyenv local dts3 dts2
  ```
  A wonderful feature is the hierarchical stucture, so for example all of python, pip and python3,
  pip3 commands resolve to the dts3 virtual environment, while only python2, pip2 resolve to the dts2
  virtual environment. 

  Another beautiful facet of oh-my-zsh in this instance is that its pyenv plugin activates and
  deactivates the virtual environment as you enter and exit the project path. No more manual
  configuration!

- **editor** vim (of course!), actually [MacVim](http://macvim-dev.github.io/macvim/) with python3
  support and the [YouCompleteMe](https://valloric.github.io/YouCompleteMe) plugin (among others).
  
