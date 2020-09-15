import os, sys, re

def shell():
    
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
                os.write(2, ("Fork failed, returning %d\n" % rc).encode())
                sys.exit(1)

            elif rc == 0:                   
                if '|' in userInput:
                    cmnd1, cmnd2 = splitPipe(userInput)

                    #Reading and Writing pipe
                    pr, pw = os.pipe()
                    for f in (pr, pw):
                        os.set_inheritable(f, True)

                    #Forking child
                    pipeFork = os.fork()
                    if pipeFork < 0:
                        print("fork failed, returning %d\n" % pipeFork, file=sys.stderr)
                        sys.exit(1)

                    elif pipeFork == 0:                   #  child - will write to pipe
                        os.close(1)                 # redirect child's stdout
                        os.dup(pw)
                        os.set_inheritable(1, True)
                        for fd in (pr, pw):
                            os.close(fd)
                        path(cmnd1)

                    else:#parent (forked ok)
                        os.close(0)
                        os.dup(pr)
                        os.set_inheritable(0, True)
                        for fd in (pw, pr):
                            os.close(fd)
                        path(cmnd2)

                elif '<' in userInput or '>' in userInput:
                    cmnd0, outFile, inFile = parse(userInput)
                    
                #if '&' at the end of the command then it should be set to run in the back 
                elif '&' in userInput[-1]:
                    exit()

                else:
                    exit()
            #wait
            else:
                waitingP = os.wait()
                    
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

        return cmd.split(), outFile, inFile)
        
def path(cmd):

    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass
        
        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error
                            
def main():
    shell()

if __name__ == "__main__":
    main()
