import os

readName = "radioCom.txt"
wrtieName = "writing.txt"

txt1 = "duishalisdufhaldsf\ndsalhfudasfdbavjbd\nasliudhfdsuail\n"
txtnum1, txtnum2, txtnum3 = "1\n", "2\n", "3\n"

list1 = ["wd", "sad", "asdas"]


def readFile(fileName):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "r")
    fileData = file.read()
    file.close()

    return fileData

def writeFile(fileName, fileText):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "w")

    for i in range(len(fileText)):
        file.write(fileText[i] + "\n")
    
    file.close()


#readeded = readFile(readName)
#readeded = readFile("pizza.txt")
#print(readeded)
writeFile(wrtieName, list1)