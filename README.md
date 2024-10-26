# Libgen CLI - books from the terminal

## Showcase
![](./showcase.gif)

## Overview
A stupid simple command-line interface for the infamous website Libgen. Allows to quickly search and install any file from the terminal without the need of a browser. It can also be argued that the cli interface is more secure, since it directly uses ![Libgen's api](https://github.com/Factual0367/libgen-api-enhanced) which means that as the end user, you do not have to worry about scam links, fishy redirects or other unwanted trackers.

## Prerequisites
* wget

## How to install
You can use the prebuilt binary instead of building and compiling from source, which will drastically simplify the setup process.
1. ```git clone https://github.com/Houdiee/libgen-cli```
2. ```mv ~/libgen-cli/dist/libgen ~/.local/bin```
3. Ensure ```~/.local/bin``` is in your system PATH

## Build from source instead of using pre-built binary
Use this option if you don't trust the prebuilt binary and would like to build it yourself.
### Modules required
* ```pip install --user libgen-api-enhanced```
* ```pip install --user prettytable```

### Converting the python file to executable
After necessary modules are installed, you can convert the python file to an executable using ```pyinstaller```:
* first clone the repo: ```git clone https://github.com/Houdiee/libgen-cli```
* then install pyinstaller: ```pip install --user pyinstaller```
* finally convert the .py file and place in system PATH: ```pyinstaller --onefile ~/libgen-cli/libgen.py```
