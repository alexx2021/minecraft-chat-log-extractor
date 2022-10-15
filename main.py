import gzip
import shutil
import os
from pathlib import Path
import time

#TODO: Add comments + console keyword input + documentation

def writeToFile(line):
    strippedLine = line.rstrip('\n')
    try:
        finalLine = strippedLine.rsplit('[Server thread/INFO]:',1)[1]
        txtFile = open("chatMessages.txt", "a", encoding="utf8")
        txtFile.write(finalLine + "\n")
        txtFile.close()
    except IndexError:
        otherMessagesTxt = open("otherMessages.txt", "a", encoding="utf8")
        otherMessagesTxt.write(line + "\n")
        otherMessagesTxt.close()



currentDir = Path.cwd()
newDir = "unzippedLogs"
newPath = os.path.join(currentDir, newDir)


try:
    os.mkdir(newPath)
except FileExistsError:
    shutil.rmtree(newPath)
    print("Deleted the old \"unzippedLogs\" Dir")
    os.mkdir(newPath)
    time.sleep(2)




files = Path("./logs").glob('*.log.gz')
for file in sorted(files):
    print(f"Unzipping {file.name}...")

    with gzip.open(f"./logs/{file.name}","rb") as f_in, open(f"./unzippedLogs/{file.name.rsplit('.',1)[0]}","wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    logFile = open(f"{newPath}/{file.name.rsplit('.',1)[0]}", "r", encoding="utf8")
    print(f"Processing {file.name}...")
    for line in logFile:
        if ("<" in line) and (">" in line):
            if not "com.mojang.authlib" in line:
                writeToFile(line)
        elif "left the game" in line:
            writeToFile(line)
        elif "joined the game" in line:
            writeToFile(line)
        elif "to the whitelist" in line:
            writeToFile(line)
        

    logFile.close()
print("Clearing the directory unzippedLogs...")
shutil.rmtree(newPath)
print("Done.")

