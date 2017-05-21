import requests
# Quick And Dirty Config------------------------------------------------------------------------ #
client_id = 'CHANGEME'
client_token = 'CHANGEME'
site = 'http://towerofawesome.org/railcraftpack'
#  --------------------------------------------------------------------------------------------- #
if "CHANGEME" in [client_token, client_id]:
    print("please Retrieve the client id and token and paste it Above : "
          "http://towerofawesome.org/railcraftpack/api/new_client.php")
    input()
with open('pack.version', 'r') as v:
    version = v.readlines()
sitever = requests.get(site + '/api/current')
print('Site Version: ' + str(sitever.text))
print('local Version: ' + version[0])
if float(version[0]) < float(sitever.text):
    # Theres an update!
    print("Update Available! : '" + str(sitever.text) + "' Do you wish to update?")
    xin = "y"
    if 'y' in xin:
        # Theres an update and the player wants it. Retrieve the tokens!
        payload = {'client_id': client_id, 'client_secret': client_token}
        print('Retrieving Token!')
        auth = requests.post(site + '/api/auth/', payload)
        token = None
        try:
            jsonResult = auth.json()
            token = jsonResult["token"]
            if jsonResult["result"] is not 0:
                if jsonResult["result"] == 6:
                    #  Something went wrong!(Timed out)
                    #  Lets try using the old token...
                    print("Failed to retrieve Token. Using old token...")
                    with open('tokens', 'r') as t:
                        token = t.readlines()
                        for string in token:
                            token = string
                        t.close()
        except ValueError:
            print("Cannot Decode JSON! Aborting...")
        if token is not None:
            print("Getting ID")
            payload = {'client_id': client_id, 'client_secret': client_token, 'token': token}
            geturl = requests.post(site + "/api/get_download_url/", payload)
            urljson = geturl.json()
            bytesize = urljson["size_raw"]
            if urljson["result"] == 0:
                print("Success!")
                print("Getting Download...")
                # pass the id! we are through!
                id = urljson['id']
                print(id, token)
                payload2 = {'client_id': client_id, 'client_secret': client_token, 'token': token,
                            'id': id}
                print("Downloading...")
                file = requests.post(site + "/api/get_file/", payload2, stream=True)
                with open('modpack.zip', 'wb')as mpf:
                    mpf.write(file.content)
                print('Downloaded!')
                with open('tokens', 'w') as t:
                    t.write(token)
            else:
                print("The updated didn't manage to get the id :/")
                print(urljson["error"])
else:
    print("Current Pack is up-to-date!")
