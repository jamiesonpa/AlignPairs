import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

# region
ArabidopsisSequenceNames = []
ArabidopsisSequences = []
CottonSequenceNames = []
CottonSequences = []
DataOutput = []
DataOutput.append(("SEQ1, SEQ2, ID, SIM"))

with open("C:\\Users\\Pierce\\Desktop\\Pairwise Alignment\\Arabidopsis Sequences.txt") as file:
    ArabidopsisFile = file.read()
    SequenceSplit = ArabidopsisFile.split("\n")
    counter = 0
    for seq in SequenceSplit:
        if counter % 2 == 0:
            ArabidopsisSequenceNames.append(seq)
        else:
            ArabidopsisSequences.append(seq)
        counter = counter + 1

ArabidopsisSequenceTuples = []

counter2 = 0
while counter2 < (len(ArabidopsisSequenceNames)-1):
    ArabidopsisSequenceTuples.append(
        (ArabidopsisSequenceNames[counter2], ArabidopsisSequences[counter2]))
    counter2 = counter2 + 1

with open("C:\\Users\\Pierce\\Desktop\\Pairwise Alignment\\CottonSequences.txt") as file:
    CottonFile = file.read()
    SequenceSplit = CottonFile.split("\n")
    counter = 0
    for seq in SequenceSplit:
        if counter % 2 == 0:
            CottonSequenceNames.append(seq)
        else:
            CottonSequences.append(seq)
        counter = counter + 1

CottonSequenceTuples = []

counter2 = 0
while counter2 < (len(CottonSequenceNames)-1):
    CottonSequenceTuples.append(
        (CottonSequenceNames[counter2], CottonSequences[counter2]))
    counter2 = counter2 + 1
url = "https://www.ebi.ac.uk/Tools/psa/emboss_needle/"
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
driver = webdriver.Firefox(
    capabilities=cap, executable_path="C:\\Users\\Pierce\\Desktop\\interproscan\\geckodriver.exe")
driver.get(url)
driver.maximize_window()

# endregion


def extractRelevantData(pfts):
    split1 = pfts.split("Identity")
    split2 = split1[1].split("Gaps")
    split3 = split2[0].split(")")
    Identity = (split3[0].split("("))[1]
    Similarity = (split3[1].split("("))[1]
    # print("Printing split3")
    # print(split3)
    # print("printing Identity")
    # print(Identity)
    # print("printing Similarity")
    # print(Similarity)
    return((Identity, Similarity))


def compareSequences(sequencetuple1, sequencetuple2):
    methodrunning = True
    while methodrunning == True:
        driver.execute_script("window.scrollTo(0,400)")
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
            (By.ID, 'asequence')))
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
            (By.ID, 'bsequence')))
        abox = driver.find_element_by_id('asequence')
        abox.send_keys(sequencetuple1[1])
        bbox = driver.find_element_by_id('bsequence')
        bbox.send_keys(sequencetuple2[1])
        time.sleep(.3)
        driver.execute_script("window.scrollTo(0,1000)")
        xpathstring = (
            "//*[@id=" + "\"" + "jd_submitButtonPanel" + "\"" + "]/input")
        time.sleep(1)
        button = driver.find_element_by_xpath(xpathstring)
        button.click()

        pageloaded = False

        while pageloaded == False:
            try:
                preformattedtextstring = driver.find_element_by_xpath(
                    ".//pre").text
                pageloaded = True
            except:
                time.sleep(1)
                #print("Page Loading")
        relevantdata = extractRelevantData(preformattedtextstring)
        print("Sequence 1: " + sequencetuple1[0] + ", " + "Sequence 2: " + sequencetuple2[0] +
              ", " + "Identity: " + relevantdata[0] + "Similarity: " + relevantdata[1])
        DataOutput.append(
            (sequencetuple1[0] + "," + sequencetuple2[0] + "," + relevantdata[0] + "," + relevantdata[1]))

        driver.get(url)
        with open("C:\\Users\\Pierce\\Desktop\\Pairwise Alignment\\output.txt", "a+") as output:
            output.write((sequencetuple1[0] + "," + sequencetuple2[0] +
                          "," + relevantdata[0] + "," + relevantdata[1] + "\n"))
        time.sleep(3)

        methodrunning = False


for asequence in ArabidopsisSequenceTuples:
    for bsequence in CottonSequenceTuples:
        compareSequences(asequence, bsequence)
