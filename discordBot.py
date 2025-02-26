import requests

def updateServer(shipName,loc,status,profits,action,inventory,fuel,cycleProfits = None):
    body = {
        "embeds":[{
            "title": shipName,
            "fields":[
                {
                    "name":"Current Location:",
                    "value" : loc,
                    "inline":True,
                },
                {
                    "name":"Flight Status:",
                    "value" : status,
                    "inline":True,
                },
                {
                    "name":"Current Profits:",
                    "value" : profits,
                    "inline": True
                },
                {
                    "name": "Cycle Profits",
                    "value": cycleProfits,
                    "inline":True
                },
                {
                    "name":"Current Action:",
                    "value": action
                },
                {
                    "name":"Inventory:",
                    "value" : inventory,
                    "inline":True,
                },
                {
                    "name":"fuel:",
                    "value" : fuel,
                    "inline":True,
                }

            ]
        }]
    }

    if shipName == "TESTING19283-1":
        url = 'https://discord.com/api/webhooks/1260195325097021520/DlbJcekO1F_ea7x62u4BFihhQv1KlUxRln5_OxmTJyyqpa1_ydNzkawxfQ-eJfVUOiTW/messages/1260197861434593363'
        response = requests.patch(url,json=body)
        second_url = 'https://discord.com/api/webhooks/1259776324298604615/-Hyhp5rZUYUsLUvfJs34g0_ifguH1hnBAghori7hmB_ujT2FfIsjk5NSH_9RPetCPN5w?wait=true'
        second_response = requests.post(second_url,json=body)
    elif shipName == "TESTING19283-1B":
        url = 'https://discord.com/api/webhooks/1260195325097021520/DlbJcekO1F_ea7x62u4BFihhQv1KlUxRln5_OxmTJyyqpa1_ydNzkawxfQ-eJfVUOiTW/messages/1260959222250602556'
        response = requests.patch(url,json=body)
        second_url = 'https://discord.com/api/webhooks/1259776324298604615/-Hyhp5rZUYUsLUvfJs34g0_ifguH1hnBAghori7hmB_ujT2FfIsjk5NSH_9RPetCPN5w?wait=true'
        second_response = requests.post(second_url,json=body)
    elif shipName == "TESTING19283-1C":
        url = 'https://discord.com/api/webhooks/1260195325097021520/DlbJcekO1F_ea7x62u4BFihhQv1KlUxRln5_OxmTJyyqpa1_ydNzkawxfQ-eJfVUOiTW/messages/1260959317767749642'
        response = requests.patch(url,json=body)
        second_url = 'https://discord.com/api/webhooks/1259776324298604615/-Hyhp5rZUYUsLUvfJs34g0_ifguH1hnBAghori7hmB_ujT2FfIsjk5NSH_9RPetCPN5w?wait=true'
        second_response = requests.post(second_url,json=body)
    else:
        url = 'https://discord.com/api/webhooks/1259776324298604615/-Hyhp5rZUYUsLUvfJs34g0_ifguH1hnBAghori7hmB_ujT2FfIsjk5NSH_9RPetCPN5w?wait=true'
        response = requests.post(url,json=body)
