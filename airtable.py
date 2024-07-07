import requests
from datetime import datetime
import random

def get_Records(status=None) -> list:
    token = "Bearer patQdvIlSL2wyhMm7.81f819a5ec1358f25c3f1518c3e58a8cdc19630e0697856e84315de4848f2051"
    base = "appMcOq1kncqafleI"
    table = "tbloLozTMGyG4s2wp"
    url = f"https://api.airtable.com/v0/{base}/{table}"
    header={"Authorization": token}

    data = requests.get(
        url=url,
        headers=header
    )

    if data.status_code == 200:
        records = list(map(lambda x: x.get("fields"), data.json().get("records")))
        records = list(map(lambda x: {**x, "Created": datetime.strptime(x.get("Created"), "%Y-%m-%dT%H:%M:%S.%fZ")}, records))
        records.sort(key=lambda x: x.get("Created"))
        if status:
            return list(filter(lambda x: x.get("Status")==status, records))
        
        else:
            return records

    else:
        return "Error"


def update_Record(id: str, content: dict):
    token = "Bearer patQdvIlSL2wyhMm7.81f819a5ec1358f25c3f1518c3e58a8cdc19630e0697856e84315de4848f2051"
    base = "appMcOq1kncqafleI"
    table = "tbloLozTMGyG4s2wp"
    url = f"https://api.airtable.com/v0/{base}/{table}/{id}"
    header={
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data_content={
        "fields": content
    }
    
    response = requests.patch(
        url=url,
        headers=header,
        json=data_content
    )

    if response.status_code == 200:
        return "Successful"
    else:
        return "Error"


def create_Record(content: dict):
    token = "Bearer patQdvIlSL2wyhMm7.81f819a5ec1358f25c3f1518c3e58a8cdc19630e0697856e84315de4848f2051"
    base = "appMcOq1kncqafleI"
    table = "tbloLozTMGyG4s2wp"
    url = f"https://api.airtable.com/v0/{base}/{table}"
    header={
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data_content={
        "records": [
            {
                "fields": content
            }
        ]
    }
    
    response = requests.post(
        url=url,
        headers=header,
        json=data_content
    )

    if response.status_code == 200:
        return "Successful"
    else:
        return "Error"


def delete_Record(recordID):
    token = "Bearer patQdvIlSL2wyhMm7.81f819a5ec1358f25c3f1518c3e58a8cdc19630e0697856e84315de4848f2051"
    base = "appMcOq1kncqafleI"
    table = "tbloLozTMGyG4s2wp"
    url = f"https://api.airtable.com/v0/{base}/{table}/{recordID}"
    header={"Authorization": token}

    response = requests.delete(
        url=url,
        headers=header
    )

    if response.status_code == 200:
        return "Successful"
    else:
        return "Error"



def chosen_color():
    colors_list = ["BROWN", "PINK", "RED", "AMBER", "INDIGO", "GREEN", "PURPLE"]
    return random.choice(colors_list)


if __name__ == "__main__":
    
    a = get_Records()
    # datestring = a[0].get("Created")
    # print(datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S.%fZ"))
    print(a)
    