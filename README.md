# Load Times Scraper

Python script used for load times analysis.
This script was created for and used in the **VŠE 4SA526 New Media and Social Networks** class project.

# What it is

This script simply iterates over a list of domains in websites.txt and generates HAR (HTTP Archive) files. Script then parses each individual HAR file and generates a parsed file that displays each website's total load time.

A sample websites.txt file is in directory, you may modify this file according to your needs.
Supported extensions are as follows:

 1. Adblock **ver. 5.4.1.0**
 2. Adblock Plus **ver. 3.16.2.0**
 3. Ghostery **ver. 8.9.14.0**
 4. Privacy Badger **ver. 2023.1.31.0**
 5. uBlock Origin **ver. 1.48.4.0**

# Usage

Navigate into project directory and run the script:

    python script.sh [extension_name=adblock|adblockplus|ghostery|privacy|ublock|false] [verbose=true|false]

The command `verbose` dumps the HAR files in the relative directory, so you can inspect them yourselves.

# Requirements

 1. Python 2.7

Any other plugin requirements (chromedriver, browsermob-proxy, extension .crx files) are provided in the project directory.