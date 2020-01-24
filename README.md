# BringTrack v1.0
BringTrack is a script that lets you track packages sent or handeled by Bring (Norwegian postal service). The script uses Bring's own API to fetch details. 

## Usage
The scripts needs a tracking number as agument. 
```
./bringtrack [TRACKING_NUMBER]
```
## Output
```
Looking up tracking detail for XXXXXXXXXXXXXX

Tracking details for XXXXXXXXXXXXXX
___________________________________________
Shipment number: 1111111111111111
Product Name: NORGESPAKKE EGENEMBALLERT
Weight: 1.2 kg
Dimensions: 37 x 22 x 7 cm
Total volume: 5.7 dm3
___________________________________________


History:
-------------------------------------------
24.01.2020 10:48
Location: 0024 OSLO, Norway
Status: IN_TRANSIT
Description: The shipment is in transit
----
24.01.2020 06:06
Location: 0024 OSLO, Norway
Status: IN_TRANSIT
Description: The shipment has been sorted and forwarded.
----
23.01.2020 18:47
Location: 5020 BERGEN, Norway
Status: IN_TRANSIT
Description: The shipment has been handed in at terminal and forwarded.
----
23.01.2020 14:04
Location: 5341 STRAUME, Norway
Status: HANDED_IN
Description: The shipment has been handed in to Bring.
----
```
## Requirements
- Python 3 
- Requests library installed 
- sys library installed 
