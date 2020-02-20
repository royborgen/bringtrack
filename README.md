# BringTrack
BringTrack is a script that lets you track packages sent or handled by Bring (Norwegian postal service). The script uses Bring's own API to fetch details. 

## Usage
The scripts needs a tracking number as agument. 
```
Usage: bringtrack [OPTION]... [TRACKING NUMBER]...
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
bringtrack -a 1234567890   Outputs all parcel details for parcel 1234567890
```
## Example output
```
Fetching data from Bring...

Latest history for 1234567890
----------------------------------------
28.01.2020 18:32
Status: DELIVERED
Description: The shipment has been delivered.
---
```
## Requirements
- Python 3 
- Requests library installed 
- sys library installed 
