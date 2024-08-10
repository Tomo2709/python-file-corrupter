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
    startRange = int(len(data) * 1/10) # avoid header
    endRange = int(len(data) * 9/10) # avoid footer

    # now lets users decide the level of corruption
    total = int(len(data))
    while True:
        try:
            i = int(input(f"\nplease enter an integer value for the amount of bytes to be changed out of the total file size({total}): "))
            if i >= 1000:
                print("better get comfy becuase we are going to be here a while!")
            elif i > total:
                print("you probably should not do that, oh well...")
            elif i == 0:
                print("what are you trying to do exactly?")
            elif i < 0:
                print("????")
            break
        except:
            print("only integers please!, try again!!")

    # core of it all right here
    # essentially, at random picks a point of the file, and then randomly generates a new value to replace the old value of that index... repeatedly.
    for bytes in range(i):
        index = random.randint(startRange, endRange-1)
        byteValue = random.randint(0,255)# generate a random interger
        binaryvalue = format(byteValue, "02x")# then convert to hex
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
