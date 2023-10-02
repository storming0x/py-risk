import requests

# Function to process data and group into risk groups
def process_data(data):
    risk_groups = {}
    
    for vault in data:
        for strategy in vault.get("strategies", []):
            risk_group = strategy.get("risk", {}).get("riskGroup")
            
            if risk_group:
                risk_group = risk_group.lower().replace(" ", "")
                if risk_group not in risk_groups:
                    risk_groups[risk_group] = {
                        "totalDebtRatio": 0,
                        "tvl": 0,
                        "strategiesCount": 0,
                        "strategies": [],
                        "oldestActivation": 0,
                        "medianScore": 0,
                        "impactScore": 0,
                        "urlParams": "",
                    }
                
                risk_groups[risk_group]["totalDebtRatio"] += strategy.get("details", {}).get("totalDebtUSDC", 0)
                risk_groups[risk_group]["tvl"] += strategy.get("details", {}).get("totalDebtUSDC", 0)
                risk_groups[risk_group]["strategiesCount"] += 1
                risk_groups[risk_group]["strategies"].append(strategy)
                
                activation = strategy.get("details", {}).get("activation", 0)
                if not risk_groups[risk_group]["oldestActivation"] or activation < risk_groups[risk_group]["oldestActivation"]:
                    risk_groups[risk_group]["oldestActivation"] = activation
    
    for risk_group in risk_groups.values():
        risk_group["longevityScore"] = 5 if not risk_group["strategies"] else get_longevity_score((current_timestamp() - risk_group["oldestActivation"]) / 86400)
        risk_group["medianScore"] = median([
            risk_group["auditScore"],
            risk_group["codeReviewScore"],
            risk_group["testingScore"],
            risk_group["protocolSafetyScore"],
            risk_group["complexityScore"],
            risk_group["teamKnowledgeScore"],
            risk_group["longevityScore"]
        ])
        risk_group["tvlImpact"] = get_tvl_impact(risk_group["tvl"])
        risk_group["impactScore"] = get_impact_score(risk_group["tvlImpact"], risk_group["medianScore"])
        risk_group["urlParams"] = get_exclude_include_url_params(risk_group["criteria"])
    
    return list(risk_groups.values())

# Send an HTTP GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    # Process the data and group into risk groups
    risk_groups = process_data(data)
    
    # Print the risk groups
    for group in risk_groups:
        print(group)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")


# Define the API URL
api_url = f"https://ydaemon.yearn.fi/1/vaults/all?classification=all&strategiesDetails=withDetails"

try:
    # Send an HTTP GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Print the JSON data
        print("JSON Data:")
        risk_group_data = process_data(data)
        print(risk_group_data)
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")

except Exception as e:
    # Handle exceptions, such as network errors
    print(f"An error occurred: {str(e)}")

import requests

# Define the API URL
api_url = "https://jsonplaceholder.typicode.com/posts/1"

