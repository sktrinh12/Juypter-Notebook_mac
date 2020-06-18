from urllib.request import urlopen as ureq
from shutil import copyfile
from time import sleep
import sys
import os.path.exists as exists

N_drive = "N:/tecan/sourceData/solubilization/"
local_drive = "C:/Users/NCI/Desktop/Worklists/Live in processing/"

def getPltCodeCSV(platecode):
    urllink =  "http://dataquestio.github.io/web-scraping-pages/simple.html" #{platecode}
    #print(urllink.read())
    page = str(ureq(urllink).read()).strip()
    sleep(0.5)
    if 'true' in page:
        # copyfile("/Users/spencertrinh/GitRepos/chemITry/requirements.txt", f"/Users/spencertrinh/Downloads/{platecode}.csv")
        if not exists(f"{local_drive}{platecode}100.csv"):
            copyfile(f"{N_drive}{platecode}100.csv", f"{local_drive}{platecode}100.csv")

        if not exists(f"{local_drive}{platecode}200.csv"):
            copyfile(f"{N_drive}{platecode}200.csv", f"{local_drive}{platecode}200.csv")

if __name__ == "__main__":
    if len(sys.argv[1]):
        if len(sys.argv[1]) > 6:
            pltcode_substring = sys.argv[1][:8]
            getPltCodeCSV(pltcode_substring)
