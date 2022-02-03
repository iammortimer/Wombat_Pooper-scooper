#import required libraries
import time
from MATICAPI import MaticAPI

matapi = MaticAPI()
i = 1

while True:
    #get information on your wombats
    mywombats = matapi.ownedWombats()

    #no wombats found, so nothing to do
    if len(mywombats) == 0:
        print('No Wombats found on supplied address.')
        exit()

    if mywombats[0][3] >= 1:
        #We found poop to scoop!
        print(str(i) + '. Found poop to clean!')
        tx = matapi.cleanShit()
        print(str(i) + '. txid: ' + str(tx))
        print(str(i) + '. Sleeping for 24 hours, goodnight.')
        time.sleep(86400)
    else:
        print(str(i) + '. No poop, waiting for an hour.')
        time.sleep(3600)
        
    i += 1
        
