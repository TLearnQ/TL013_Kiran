import requests
import json

TOKEN="Bearer E7sKdN46eeZpdw7h0nhQ.zD79gEr7V7gDALlWMexSNc-1766213936-1.0.1.1-riFXUbo_XmHi2iKluRT6tPWUigmXbS7vYgqPnhrDRhg"
headers={
    "Authorization":f"Bearer {TOKEN}"
}

url="https://reqres.in/api/users/2"

p={
    "name":"kiran",
    "age":25
}

r=requests.put(url,p,headers=headers)
if r.status_code==200:
    data=r.json()

    with open('b.json','w')as f:
        json.dump(data,f,indent=4)
else:
    print("put is not replacing entire resources")
