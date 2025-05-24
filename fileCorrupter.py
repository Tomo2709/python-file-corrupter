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

    ext = os.path.splitext(file)[1][1:].strip().lower()
    return file, ext

# output file to write corrupted data to (this needs to be taken out and restructured)
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

# ignores header of the file and randomly replaces bytes
def corruptData(data): 
    startRange = int(len(data) * 1/10) # avoid header

    # users decide the level of corruption
    total = int(len(data))
    while True:
        try:
            i = int(input(f"\nplease enter an integer value for the amount of bytes to be changed out of the total file size({total}): "))
            if i >= 1000:
                print("This may take a while!")
            elif i == 0:
                print("what are you trying to do exactly?")
            elif i < 0:
                print("????")
            break
        except:
            print("only integers please!, try again!!")

    data = bytearray(data)

    # corruption of data
    # repeatidly picks a point in the file, and then randomly generates a new value to replace the old value of that index 
    for bytes in range(i):
        index = random.randint(startRange, total - 1)
        data[index] = random.randint(0, 255)

        # due to larger files taking forever to corrupt a progress bar is implemented to insure project is still working
        print(f"\rprogress: {i}: {bytes + 1} bytes", end="")

    return data

# write corrupted data to output write
def writeToFile(cData, output):  
    f = open(output, "wb")
    f.write(cData)  
    f.close()

# auto change file rather than user doing it manually
def changeFileExtension(ext, output, path):
    # doesnt work as intended, but does work
    changedExt = os.path.basename(output)
    changedExt = changedExt + "." + ext
    changedExt = os.path.join(path, changedExt)

    # if the file already exists iterate +1
    i = 0
    while os.path.exists(changedExt):
            changedExt = "corrupt"
            i += 1
            changedExt = os.path.join(path, f"{changedExt}{i}.{ext}")

    os.rename(output, changedExt)

def main():
    try:
        # create a directory for corrupted files
        path = "corruptFiles"
        os.mkdir(path)
        print("Directory created: ",path)
    except:
        print("folder likely already exists, proceeding...")

    file, ext = recievefile()
    print("file found!: ",file)
    output = createOutputFile(path)
    print("created file placeholder")
    data = collectData(file)
    print("binary data collected")
    cData = corruptData(data)
    print("\ndata succesffuly corrupted")
    writeToFile(cData, output)
    changeFileExtension(ext, output, path)
    print("corrupted file created please check: ", path)
main()  
