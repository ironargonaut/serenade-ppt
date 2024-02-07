#!/usr/bin/env python3
# created by Scott Olsen
# this program assumes that you have named your .js files in seranade
# the same name as the program name, example for excel the executable is 
# excel.exe so your .js file is excel.js
# all gets all commands
# windows key word assumes that windows scripts are in windows_commands.js
import re
import argparse
import ctypes  # An included library with Python install.
from tkinter import *
import os
import getpass

# this def just used for debugging since shells usually close w/o error messages
def addToClipboard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

# getting my file and my search term
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str)
parser.add_argument("-c", "--command", type=str)
args = parser.parse_args()
userpath = os.environ['USERPROFILE']
# def Mbox(title, text, style):
# find_command(commandFile)
file_path = args.file
#getting the program name only ex. excel.exe
file_name = os.path.basename(file_path)
# splitting name into to parts ex. excel and exe
name, ext = os.path.splitext(file_name)
#adding the .js to the name ex. excel.js
script_file_name = name + ".js"
# path to your serenade scripts file is added to front assumes you use default
script_full_path = os.path.join(userpath, r'.serenade\\scripts', script_file_name)
# addToClipboard(script_full_path)


def find_command(workFile, command_to_find):
    # addToClipboard(workFile)
    # addToClipboard(command_to_find)
    with open(workFile, 'r') as my_file:
      # read_data = my_file.read()
      # print('test 1')
      command_list = []
      for line in my_file:
        # print(line)
        #matches global commands
        if re.search(r'serenade.global', line):
          # when searching for "all" outputs all commands
          # "all" outputs all commands
          if command_to_find == 'all':
              # print(line)
              matched_command = re.search('"(.*)"', line)
              if matched_command:
                  command_list.append(matched_command.group(1))
          #matches lines that contain command word
          elif re.search(command_to_find, line):
              #extracts only what is in quotes in line
              #and adds this to command_list
              matched_command = re.search('"(.*)"', line)
              if matched_command:
                  command_list.append(matched_command.group(1))
        #matches app commands
        if re.search(r'serenade.app', line):
          # print(line)
          # "all" outputs all commands
          if command_to_find == 'all':
              # print(line)
              matched_command = re.search('(command\()"(.*)"', line)
              m = matched_command.group(2)
              command_list.append(m)
          #matches lines that contain command word
          elif re.search(command_to_find, line):
              # print(line)
              #extracts only what is in quotes after word command in line
              #and adds this to command_list
              matched_command = re.search('(command\()"(.*)"', line)
              # print(matched_command)   
              m = matched_command.group(2)
              # print(m)
              command_list.append(m)
    textbox(command_list)              

#creates gui w/output of commands
def textbox(myText):

    ws = Tk()
    ws.title('VoiceCommands')
    ws.geometry('550x400')
    ws.config(bg='#A67449')
    # myString = print(*myText,sep='\n')
    myString = '\n'.join(myText)
    message = myString
    
    text_box = Text(
        ws,
        height=26,
        width=60
    )
    text_box.pack(expand=True)
    text_box.insert('end', message)
        
    ws.mainloop()

#executes the command                    
find_command(script_full_path, args.command)

# if __name__ == "__main__":
#     import sys
#     find_command(int(sys.argv[1]))
