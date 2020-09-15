import os, sys, re

def userInput():
    
    while True:
        
        if 'PS1' in os.environ:
            uInput = os.environ['PS1']
        else:
            uInput = os.environ['$ ']

        #The user input is taken then split by space
        itemSplit = input(uInput)
        itemSplit = itemSplit.split(' ')

        #Depending on the user input then it will exit or change directories
        if itemSplit[0] == "exit":
            os.write(2, "Closing system".encode())
            sys.exit(0)
        if itemSplit[0] == "cd":
            try:
                os.chdir(itemSplit[1])
            except FileNotFoundError:
                os.write(2, "Directory not found".encode())
            continue
        else:
            exit()
        
        

def main():
    userInput()

if __name__ == "__main__":
    main()
