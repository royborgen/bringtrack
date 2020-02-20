#!/usr/bin/env python3
import requests
import sys

def checkarg(arg):
    version = "BringTrack 1.2"
    helptxt = """Usage: bringtrack [OPTION]... [TRACKING NUMBER]...
Fetches parcel tracking information from Bring.

   -a, --all           Outputs parcel details and complete tracking history
   -c, --consignment   Outputs consignment details
   -d, --details       Outputs parcel details
   -h, --history       Outputs full tracking history
                       Only latest entry is listed if argument if not provided 

   -v, --version       Outputs version information and exit
       --help          Displays this help text and exit

Example:
bringtrack 1234567890      Outputs latest tracking details for parcel 1234567890
bringtrack -a 1234567890   Outputs all parcel details for parcel 1234567890"""

    usage = """Usage: bringtrack [OPTION]... [TRACKING]...
Try 'bringtrack --help' for more information."""

    if len(arg) ==1: 
        return True
    elif len(arg) ==2:
        if str.startswith(str(arg[1]), "--") == True or str.startswith(str(arg[1]), "-") == True: 
            if str(arg[1]) =="--help":
                print(helptxt)
                return False
            elif str(arg[1]) =="-v" or str(arg[1]) =="--version": 
                print(version) 
                return False
            else: 
                print(usage)
                return False
        else:
            return True
    elif len(arg)==3:
        if str(arg[1]) =="-a" or str(arg[1]) =="--all":
            return "-a"
        elif str(arg[1]) =="-d" or str(arg[1]) =="--details":
            return "-d"
        elif str(arg[1]) =="-h" or str(arg[1]) =="--history":
            return "-h"
        elif str(arg[1]) =="-c" or str(arg[1]) =="--consignment":
            return "-c"
        else: 
            print(usage)
            return False
    else: 
        print(usage) 
        return False

#A function that fetches a json containing tracking info from Bring
def trackit(parcel):
    connection = True
    url = "https://sporing.posten.no"
    session = requests.Session()
    try: 
        response = session.get (url + "/tracking/api/fetch/" + parcel + "?lang=en")
    except: 
        connection = False
        print("Connection error: Unable to contact " + url)
    
    if connection == True:
        content = response.json()

        #Returns content only if results were found. 
        if response.status_code == 200: 
            return content
        else: 
            return False
    else: 
        return False


def output(arg, result):
    history = {}
    allpacks = []
    #Loops through json and prints details 
    for details in result["consignmentSet"]:
        shipnumber = str(details["consignmentId"])
        totalWeight = str(details["totalWeightInKgs"])
        totalVolume = str(details["totalVolumeInDm3"])
        numPackages = 0
        for PackageSet in details["packageSet"]:
            allpacks.append([])
            allpacks[numPackages].append("Parcel number: " + PackageSet["packageNumber"])
            allpacks[numPackages].append("Product name: " + PackageSet["productName"])
            allpacks[numPackages].append("Weight: " + str(PackageSet["weightInKgs"]) + " kg") 
            allpacks[numPackages].append("Dimentions: " + str(PackageSet["lengthInCm"]) +" x " + str(PackageSet["widthInCm"]) + " x " + str(PackageSet["heightInCm"]) + " cm")
            allpacks[numPackages].append("Total volume: " + str(PackageSet["volumeInDm3"]) + " dm3") 
            i = 1
            #history.append([])
            #history.setdefault(numPackages,[])
            #history[numPackages].append("Parcel number: " + PackageSet["packageNumber"])
            packageNumber = PackageSet["packageNumber"]
            history.setdefault(packageNumber,[])
            for eventSet in PackageSet["eventSet"]:
                #adding --- to seperate different events
                history[packageNumber].append(i)
                description = eventSet["description"] 
                #checking if description contains http (an url) 
                if description.find("http") == -1:
                    history[packageNumber].append("Description: " + description)
                else: 
                    #removing html tags and url
                    description = description[0:description.find("<")] + description[description.rfind('">')+2:description.rfind("<")]
                    history[packageNumber].append("Description: " + description)
                
                history[packageNumber].append("Status: " + eventSet["status"]) 
                
                #only prints location of "city" has value 
                if eventSet["city"] != "":
                    history[packageNumber].append("Location: "+ eventSet["postalCode"] + " " + eventSet["city"] + ", " + eventSet["country"])
                
                history[packageNumber].append(eventSet["displayDate"] + " " + eventSet["displayTime"])
                i += 1
            numPackages +=1
    
    if arg == "-c" or arg == "-a":
        print("Consignment details:")
        print("----------------------------------------")
        print("Shipment number: " + shipnumber)
        print("Number of packages: " + str(numPackages))
        print("Total weight: " + totalWeight + " kg") 
        print("Total volume: " + totalVolume + " dm3")
        print("----------------------------------------") 
        print("")
    
    if arg == "-d" or arg == "-a":
        print("Shipment contains " + str(numPackages) + " package(s):") 
        print("----------------------------------------") 
        for details in allpacks:
            for packdetail in details:
                print(packdetail) 
            print("---") 
        print("")

    if arg == "-h" or arg == "-a" or arg == True: 
        if arg == "-h" or arg =="-a": 
            for parcel, detail in history.items():
                print("Tracking history for " + parcel)
                print("----------------------------------------") 
                for value in reversed(detail):
                    if isinstance(value, int) == True: 
                        print("---")
                    else: 
                        print(value)
                print("") 
        else:
            latest = False
            for parcel, detail in history.items():
                print("Latest history for " + parcel)
                print("----------------------------------------")
             
                for value in reversed(detail):
                    if value == 2:
                        latest = True
                    else: 
                        if latest == True and value !=1: 
                            print(value)
                        if value == 1: 
                            print("---")
                print("")
                latest = False 


def main(): 
    #checking if commandline argument is provided. Only accepts one argument
    argument = checkarg(sys.argv)
    #Argument was provided
    if argument == True or argument == "-h" or argument == "-a" or argument == "-c" or argument =="-d":
        parcel = sys.argv[len(sys.argv) - 1]
        #Calls function to check for tracking details
        print("Fetching data from Bring...\n")
        result = trackit(parcel)
               
        #Gives error if no results were found
        if result == False:
            print ("No tracking information found for " + parcel)
        else: 
            output(argument, result) 
            
                 
#Calling the main function
if __name__ == "__main__":
    main()
