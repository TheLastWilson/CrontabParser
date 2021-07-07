#!/usr/bin/python
#
# Author: Craig Wilson - craigawilson@gmail.com
#
# Description: a script to parse crontab entries and present them in a neat table format
# Todo: Add support for step values
#
import sys

#Def function to check value is within acceptable range for each column
def check_range(value,column):
    if column == "Minute" and int(value) > 59:
        print ("Error: Minute column appears to exceed logical limit - " + value)
        exit()
    elif column == "Hour" and int(value) > 23:
        print ("Error: Hour column appears to exceed logical limit - " + value)
        exit()
    elif column == "DOM" and int(value) > 31:
        print ("Error: Day of Month column appears to exceed logical limit - " + value)
        exit()
    elif column == "Month" and int(value) > 12:
        print ("Error: Month column appears to exceed logical limit - " + value)
        exit()
    elif column == "DOW" and int(value) > 7:
        print ("Error: Day of week column appears to exceed logical limit - " + value)
        exit()

#Def function to parse individual elements of the crontab line
def parse_element(element,column):
    #initalise return string
    returnString = "" 
    #if element only contains * wildcard then expand wildcard according to the column that is being parsed
    if element == "*":
        if column == "Minute":
            for m in range(0,60):
                returnString += str(m) + " "
        elif column == "Hour":
            for h in range(0,24):
                returnString += str(h) + " "
        elif column == "DOM":
            for h in range(0,32):
                returnString += str(h) + " "
        elif column == "Month":
            for h in range(0,13):
                returnString += str(h) + " "
        elif column == "DOW":
            for h in range(0,8):
                returnString += str(h) + " "
    else:
        #comma indicates a list, split element based on comma to seperate list items
        elementList = str(element).split(",")
        #for element in list of elements 
        for e in elementList:
            #if range is detected in element
            if "-" in e:
                #split range entry into array to get start point [0] and end point [1] of range
                elementRange = str(e).split("-")
                #check highest value is valid according to the column being parsed
                check_range(elementRange[1],column)
                #for values inbetween start and end point of range append to returnString 
                for r in range(int(elementRange[0]),int(elementRange[1]) + 1):
                    returnString += str(r) + " "
            else:
                #check value is valid according to the column being parsed
                check_range(e,column)
                returnString += e + " "
    return returnString
        
### Start menu program ###

# Get the total number of args
total = len(sys.argv)
 
#if length more than 2 arguments then crontab entry hasn't been escaped, print error and exit
if len(sys.argv) > 2:
    print "too many arguments, please escape crontab entry with quotation marks"
    exit()

cmdargs = ""
if len(sys.argv) == 2:
    # Get the arguments list 
    cmdargs = str(sys.argv[1]).split()

if len(cmdargs) < 6:
    print "Crontab entry does not appear to be long enough, only %d elements detected" % len(cmdargs)
    exit()

# Print it
# print ("The total numbers of args passed to the script: %d" % total)
# print ("Args list: %s " % cmdargs)
# print

print ("Minute \t\t" + str(parse_element(cmdargs[0],"Minute")))
print ("Hour \t\t" + str(parse_element(cmdargs[1],"Hour")))
print ("Day of month \t" + str(parse_element(cmdargs[2],"DOM")))
print ("Month \t\t" + str(parse_element(cmdargs[3],"Month")))
print ("Day of Week \t" + str(parse_element(cmdargs[4],"DOW")))

# user remaining array elements to form the command string
commandString = ""
for i in range(5,len(cmdargs)):
    commandString += str(cmdargs[i]) + " "
print ("Command \t" + commandString)