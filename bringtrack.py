#!/usr/bin/env python3
import requests
import sys

#A function that fetches a json containing tracking info from Bring (Posten) 
def traceit(parcel):
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


def main(): 
    #Variable to be used for checking if a commandline argument was provided 
    argument = False
    
    #checking if commandline argument is provided. Only accepts one argument
    if len(sys.argv) == 2: 
        parcel = sys.argv[1]
        argument = True
    else: 
        #Gives instructions if no arguments were provided
        print("You must supply a tracking number!") 
        print("To run the script type " + sys.argv[0] + " [TRACKING_NUMBER]") 
    
    #Argument was provided
    if argument == True:
        #Calls function to check for tracking details
        print("Looking up tracking detail for " + parcel)
        result = traceit(parcel)
        
        #Gives error if no results were found
        if result == False:
            print ("No tracking information found for " + parcel)
        else: 
            #Prints detail
            print("\nTracking details for " + parcel)
            print("___________________________________________")
            
            #Loops through json and prints details 
            for details in result["consignmentSet"]:
                print("Shipment number: " + str(details["consignmentId"]))
                for PackageSet in details["packageSet"]:
                    print("Product Name: " + PackageSet["productName"])
                    print("Weight: " + str(PackageSet["weightInKgs"]) + " kg") 
                    print("Dimensions: " + str(PackageSet["lengthInCm"]) +" x " + str(PackageSet["widthInCm"]) + " x " + str(PackageSet["heightInCm"]) + " cm") 
                    print("Total volume: " + str(PackageSet["volumeInDm3"]) + " dm3") 

                    print("___________________________________________\n")
                    print("\nHistory:")
                    print("-------------------------------------------") 
                    for eventSet in PackageSet["eventSet"]:
                    
                        print(eventSet["displayDate"] + " " + eventSet["displayTime"])  
                        print("Location: " + eventSet["postalCode"] + " " + eventSet["city"] + ", " + eventSet["country"]) 
                        print("Status: " + eventSet["status"]) 
                        print("Description: " + eventSet["description"])
                        print("----") 


#Calling the main function
if __name__ == "__main__":
    main()
