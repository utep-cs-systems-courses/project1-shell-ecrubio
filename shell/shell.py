import os, sys, re

def userInput():
    
    while True:
        
        if 'PS1' in os.environ:
            uInput = os.environ['PS1']
        else:
            uInput = os.environ['$ ']

        #The user input is taken then split by space
        userInput = input(uInput)
        itemSplit = userInput.split(' ')

        #Depending on the user input then it will exit or change directories
        if itemSplit[0] == "exit":
            os.write(2, "Closing system".encode())
            sys.exit(1)
        if itemSplit[0] == "cd":
            try:
                os.chdir(itemSplit[1])
            except FileNotFoundError:
                os.write(2, "Directory not found".encode())
            continue
        #Forking
        else:
            rc = os.fork()
            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc == 0:                   
                if '|' in userInput:
                    cmnd1, cmnd2 = splitPipe(userInput)

                    #Reading and Writing pipe
                    rPipe, wPipe = os.pipe()
                elif '<' in userInput or '>' in userInput:
                    cmnd0, outFile, inFile = parse(userInput)
                #if '&' at the end of the command then it should be set to run in the back 
                elif '&' in userInput[-1]:
                    exit()
                else:
                    exit()
            #wait
            else:
                exit()
                    
#Splitting the pipe commands
def splitPipe(userInput):
    pipe = userInput.split('|')
    return pipe[0].strip(), pipe[1].strip()

#Code from Professor(TEAMS code)
def parse(cmdString):
        outFile = None
        inFile = None
        cmd = ''

        cmdString = re.sub(' +', ' ', cmdString)
        if '>' in cmdString:
            [cmd, outFile] = cmdString.split('>',1)
            outFile = outFile.strip()

        if '<' in cmd:
            [cmd, inFile] = cmd.split('<', 1)
            inFile = inFile.strip()

        elif outFile != None and '<' in outFile:
            [outFile, inFile] = outFile.split('<', 1)
            outFile = outFile.strip()
            inFile = inFile.strip()

        return cmd.split(), outFile, inFile

def main():
    userInput()

if __name__ == "__main__":
    main()
