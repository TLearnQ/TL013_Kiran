import requests
import json

# Your existing credentials and headers
TOKEN = "Bearer E7sKdN46eeZpdw7h0nhQ.zD79gEr7V7gDALlWMexSNc-1766213936-1.0.1.1-riFXUbo_XmHi2iKluRT6tPWUigmXbS7vYgqPnhrDRhg"
headers = {
     "Authorization": f"Bearer {TOKEN}",
 }

url = "https://reqres.in/api/users/2"
responses = requests.get(url, headers=headers)


data = {
         "job":"oracle"
     }

response = requests.post(url, json=data, headers=headers)
response = requests.put(url, json=data, headers=headers) 
# Check if the request was successful
if responses.status_code == 200:
     data = responses.json()
    
#    # Save to a JSON file
     with open('task4.json', 'w', encoding='utf-8') as f:
         json.dump(data, f, indent=4)
    
     print("Status Code:", responses.status_code)
     print("Success! Response saved to 'task4.json'")
else:
     print(f"Error: {responses.status_code}")
     print(responses.text)

json_data = response.json()
json_str = json.dumps(json_data, indent=4)
print("json POST response body: ", json_str)


