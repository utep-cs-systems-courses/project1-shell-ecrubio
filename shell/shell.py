#!/usr/bin/env python3

import os, sys, re

def redirect(cmnd):
    if '>' in cmnd:
        os.close(1)
        os.open(cmnd[cmnd.index('>') + 1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        cmnd.remove(cmnd[cmnd.index('>') + 1])
        cmnd.remove('>')

    else:
        os.close(0)
        os.open(cmnd[cmnd.index('<') + 1], os.O_RDONLY)
        os.set_inheritable(0, True)
        cmnd.remove(cmnd[cmnd.index('<') +1])
        cmnd.remove('<')

    for dir in re.split(":", os.environ['PATH']):
        prog = "%s/%s" % (dir, cmnd[0])
        try:
            os.execve(prog, cmnd, os.environ)
        except FileNotFoundError:
            pass

    os.write(2, ("Command not found \n").encode())
    sys.exit(1)

def execute(cmnd):
    if '>' in cmnd or '<' in cmnd:
        redirect(cmnd)
    elif '/' in cmnd[0]:
        try:
            os.execve(cmnd[0], cmnd, os.environ)
        except FileNotFoundError:
            pass
    else:
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmnd[0])
            try:
                os.execve(prog, cmnd, os.environ)
            except FileNotFoundError:
                pass
    os.write(2, ("Command not found \n").encode())
    sys.exit(1)

def piping(cmnd):
    write = cmnd[0:cmnd.index("|")]
    read = cmnd[cmnd.index("|") + 1:]

    pr, pw = os.pipe()
    rc = os.fork()

    #forked failed
    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        #close output
        os.close(1)
        os.dup(pw)
        #output to pipe
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)
        execute(write)
        os.write(2, ("Could not exec %s\n" % write[0]).encode())
        sys.exit(1)
    else:
        os.close(0)
        os.dup(pr)
        #input to pipe
        os.set_inheritable(0, True)
        for fd in (pr, pw):
            os.close(fd)
        if "|" in read:
            piping(read)
        execute(read)
        os.write(2, ("Could not exec %s\n" % read[0]).encode())
        sys.exit(1)

def readCommand(cmnd):
    if len(cmnd) == 0:
        return
    elif cmnd[0] == 'exit':
        os.write(1, ("Goodbye\n").encode())
        sys.exit(0)

    elif cmnd[0] == 'cd':
        try:
            if len(cmnd) == 1:
                os.chdir("..")
            else:
                os.chdir(cmnd[1])
        except FileNotFountError:
            os.write(1, ("The directory " + cmnd[1] + " does not exist.").encode())
            
    elif "|" in cmnd:
        piping(cmnd)
    else:
        rc = os.fork()
        
        wait = True
        if "&" in cmnd:
            cmnd.remove("&")
            wait = False
        if rc < 0:
            os.write(2, ("Fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        #child
        elif rc == 0:
            execute(cmnd)
            sys.exit(0)
        #parent >
        else:
            if wait:
                childpid = os.wait()

def shell():    
    while True:

        if 'PS1' in os.environ:
            os.write(1, os.environ['PS1'].encode())
        else:
            os.write(1, ('$ ').encode())

        try:
            userInput = os.read(0, 10000)

            if len(userInput) == 0:
                break
            userInput = userInput.decode().split("\n")

            if not userInput:
                continue
            for cmnd in userInput:
                readCommand(cmnd.split())
        except EOFError:
            sys.exit(1)
            
                            
def main():
    shell()

if __name__ == "__main__":
    main()
