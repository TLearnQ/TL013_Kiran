import yaml  
import json


try:
    with open("CommonData.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    with open("CommonData.json", "w") as json_file:
        
        json.dump(data, json_file, indent=4)

    print("Converted 'CommonData.yaml' to 'CommonData.json'")
    

    print("\n--- JSON OUTPUT PREVIEW ---")
    print(json.dumps(data, indent=4)[:500] + "\n...")

except FileNotFoundError:
    print("Error: The file 'CommonData.yaml' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")