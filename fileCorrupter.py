import os
import sys
import random

# recieves and checks validity of file/file path
def recievefile():
    file = ""
    while True:
        try:
            file = input("please enter a valid path: ")
            # attempt to open file, go to except state if fail
            f = open(file, "r")
            f.close()
            # if succsefull break while loop
            break
        except:
            print("cannot find file, or file does not exist: ")
            while True:
                choice = input("try again? y/n")
                if choice == "y":
                    break
                elif choice == "n":
                    sys.exit()
                else:
                    print("invalid entry")

    return file

# we need an output file to write corrupted data to
def createOutputFile(path):
    filename = "corrupt"
    filename = os.path.join(path, f"{filename}.bin")

    # if the file already exists iterate +1
    i = 0
    while os.path.exists(filename):
            filename = "corrupt"
            i += 1
            filename = os.path.join(path, f"{filename}{i}.bin")

    #create file       
    with open (filename, "w") as f:
        f.write("hello world")  
    f.close()

    return filename

# reads binary data from file and stores it
def collectData(file):
    f = open(file, "rb")
    data = f.read()
    f.close()

    return data

# ignores header and footer of the file and randomaly replaces bytes
def corruptData(data):
    startRange = int(len(data) * 1/6) # avoid header
    endRange = int(len(data) * 5/6) # avoid footer

    # effectively we have 4/6 of the file to work with, however note these values are based purely on supistition(i have no idea how large file headers are)
    # added proportional scaling to the range of corruption, however feel free to change this if you dont get desired results
    total = int(len(data) * 4/6)
    i = int(total * 0.00025) # changed range slightly for faster corruption, now scales to 4/6 of the data rather than the whole thing
    for bytes in range(i):
        index = random.randint(startRange, endRange-1)
        byteValue = random.randint(0,255)
        binaryvalue = format(byteValue, "02x")
        data = data[:index] + binaryvalue.encode() + data[index+2:]
        # due to larger files taking forever to corrupt a progress bar is implemented to insure project is still working
        print(f"\rprogress: {i}: {bytes} bytes", end="")

    return data

# remember the output file that stores hello world, yeah we write the corrupted data to that
def writeToFile(cData, output):  
    f = open(output, "wb")
    f.write(cData)  
    f.close()

def main():
    try:
        # create a directory for corrupted files
        # directory is now created locally, rather than needing a specific path
        directory = "corruptFiles"
        path = directory
        os.mkdir(path)
        print("Directory created: ",path)
    except:
        print("folder likely already exists, proceeding...")

    file = recievefile()
    print("file found!: ",file)
    output = createOutputFile(path)
    print("created file placeholder")
    data = collectData(file)
    print("binary data collected")
    cData = corruptData(data)
    print("\ndata succesffuly corrupted")
    writeToFile(cData, output)
    print("corrupted file created please check: ",path)
    print("to see the results make sure you rename the file back to its original file format, and also ingore the warnings(trust me)")

main()  
