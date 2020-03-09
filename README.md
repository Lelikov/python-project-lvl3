[![Maintainability](https://api.codeclimate.com/v1/badges/4a13b6d00865ea2afc5f/maintainability)](https://codeclimate.com/github/Lelikov/python-project-lvl3/maintainability)
[![Build Status](https://travis-ci.org/Lelikov/python-project-lvl3.svg?branch=master)](https://travis-ci.org/Lelikov/python-project-lvl3)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a13b6d00865ea2afc5f/test_coverage)](https://codeclimate.com/github/Lelikov/python-project-lvl3/test_coverage)
# Page loader
Utility for loading web page.
## Install
```
pip install lelikov-page_loader --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple
```
## Use
```
page-loader URL -o PATH -l LOGGING LEVEL
```
## Logging level
```
- Debug
- Info
- Warning
- Error
- Critical
```
##Exit error codes
```
2 - failed to download page
3 - failed to download file
4 - failed to make directory
5 - failed to save file
6 - failed to save page
```
##Use without positional arguments
[![asciicast](https://asciinema.org/a/ZF08zlJHfFiFOQi7vd35ghViX.svg)](https://asciinema.org/a/ZF08zlJHfFiFOQi7vd35ghViX)
##Use with positional arguments
[![asciicast](https://asciinema.org/a/Vtey51hdner7jLE3vkL3hw7vZ.svg)](https://asciinema.org/a/Vtey51hdner7jLE3vkL3hw7vZ)
##Error processing
[![asciicast](https://asciinema.org/a/S2niHF3LjdQFoSuaL75Q7vLJQ.svg)](https://asciinema.org/a/S2niHF3LjdQFoSuaL75Q7vLJQ) 