#!/usr/bin/python
from browsermobproxy import Server
from selenium import webdriver
import os
import json
import urlparse,sys;
import logging 
import json
from haralyzer import HarParser, HarPage

# mobile_or_not = sys.argv[1]; # mobile or not
extension = sys.argv[1]; # extension name
verbose = sys.argv[2]; # also dump har file

dirname = os.path.abspath(".")

# path to browsemob-proxy 
server = Server(os.path.join(dirname, "browsermob-proxy/bin/browsermob-proxy"))
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()

chromedriver = os.path.join(dirname, "chromedriver.exe")
os.environ["webdriver.chrome.driver"] = chromedriver
url = urlparse.urlparse (proxy.proxy).path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(url))

output_folder = "data"

# if(mobile_or_not=="mobile"):
# 	mobile_emulation = {'deviceName': 'Google Nexus 5'}
# 	chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# 	output_folder += "_mobile"

if(extension=="adblock"):
	chrome_options.add_extension(os.path.join(dirname, "Adblock_v5.4.1.0.crx"))
	output_folder += "_with_adblock"
elif(extension=="adblockplus"):
	chrome_options.add_extension(os.path.join(dirname, "Adblock-Plus_v3.16.2.0.crx"))
	output_folder += "_with_adblockplus"
elif(extension=="ghostery"):
	chrome_options.add_extension(os.path.join(dirname, "Ghostery_v8.9.14.0.crx"))
	output_folder += "_with_ghostery"
elif(extension=="privacy"):
	chrome_options.add_extension(os.path.join(dirname, "Privacy-Badger_v2023.1.31.0.crx"))
	output_folder += "_with_privacy_badger"
elif(extension=="ublock"):
	chrome_options.add_extension(os.path.join(dirname, "uBlock-Origin_v1.48.4.0.crx"))
	output_folder += "_with_ublock"

chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options = chrome_options)
driver.set_page_load_timeout(20)

f = open(os.path.join(dirname, "websites.txt"))
lines = f.readlines()

out = open(output_folder + "/" + "parsed.json", "a")
out.write("============================================\n")

for line in lines:
    line = line.strip()
    url = "https://www." + line
    print >> sys.stderr, "processing", url
    try:
        proxy.new_har(url)
        driver.get(url)
        result = json.dumps(proxy.har, ensure_ascii=False)
        if (verbose == "1"):
            out = open(output_folder + "/" + line.replace("/","_") + ".json", "w")
            out.write(result.encode('utf-8'))
            out.close()
        har_parser = HarParser(json.loads(result))
        total_load_time = 0
        for page in har_parser.pages:
         total_load_time += page.get_load_time(status_code='2.*')
        out = open(output_folder + "/" + "parsed.json", "a")
        out.write(line + ": " + str(total_load_time) + ' ms \n')
        out.close()
    except Exception as e:
        logging.error('Error at %s', line, exc_info=e)
        print >> sys.stderr, "skipped", url
        pass

#    break;
#proxy.stop()
driver.quit()
