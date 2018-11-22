# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Laptop"
__date__ = "$19.11.2018 14:06:27$"

import shodan
# create Shodan API
SHODAN_API_KEY = "V8kcW56VkPG3xF5modxydH45wPY0W7ft"

api = shodan.Shodan(SHODAN_API_KEY)

# Wrap the request in a try/ except block to catch errors
try:
        #Eingabe User
        query = input("Bitte geben Sie ihre Anfrage ein: ")
        
        # Search Shodan
        results = api.search(query)

        # Show the results
        print('Results found: {}'.format(results['total']))
        for result in results['matches']:
                file = open("Ergebnis.txt","a")
                #file.write("/n. result")
                file.write('\nIP: {}'.format(result['ip_str']))
                file.write('\nPort: {}'.format(result['port']))
                file.write('\nOrganisation: {}'.format(result['org']))
                file.write('\nBetriebsystem: {}'.format(result['os']))
                file.write('\nLand: {}'.format(result['location']))
                file.write('')
                file.write('\n')
                
       
        
except shodan.APIError. e:
        print('Error: {}'.format(e))
