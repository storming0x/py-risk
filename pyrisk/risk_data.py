import requests
import time

def get_risk_data(chainId=1):
    url = f"https://ydaemon.yearn.fi/{chainId}/vaults/all?classification=all&strategiesDetails=withDetails"
    response = requests.get(url)
    risk_data = response.json()
    data_matrix = process_data(risk_data)

    return data_matrix

# TODO: fetch data from ydaemon and aggregate into risk groups to create data matrix
# TODO: use yearn watch logic to do the aggregation
def get_risk_data_hardcoded(chainid=1):
    data_matrix = [
        ["", "Convex", "", "", ""],
        ["", ["Curve", "Generic Lev Comp", "Single Sided"], "", "", ""],
        ["", ["AAVE Lender Borrower", "Router Strategy", "stETH Accumulator", "yvBoost", "Notional Lending"], "Gen Lender", "Angle Protocol", ""],
        ["","Single Sided Balancer v3",["Maker", "Synthethix", "Strategy Tokemak", "88mph deposit"], "Stargate", ""],
        ["", ["Maker V2", "Idle", "Alpha Homora v2"], "Vesper", "Inverse", ""],
    ]

    return data_matrix

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
                        "label": risk_group,
                        "totalDebtRatio": 0,
                        "tvl": 0,
                        "strategiesCount": 0,
                        "strategies": [],
                        "oldestActivation": 0,
                        "medianScore": 0,
                        "impactScore": 0,
                        "urlParams": "",
                        "auditScore": strategy.get("risk", {}).get("auditScore", 0),
                        "codeReviewScore": strategy.get("risk", {}).get("codeReviewScore", 0),
                        "testingScore": strategy.get("risk", {}).get("testingScore", 0),
                        "protocolSafetyScore": strategy.get("risk", {}).get("protocolSafetyScore", 0),
                        "complexityScore": strategy.get("risk", {}).get("complexityScore", 0),
                        "teamKnowledgeScore": strategy.get("risk", {}).get("teamKnowledgeScore", 0),
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
        #risk_group["urlParams"] = get_exclude_include_url_params(risk_group["criteria"])
    
    data_matrix = create_data_matrix(list(risk_groups.values()))
    print(data_matrix)
    return data_matrix




def create_data_matrix(groups):
    data_matrix = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]

    for group in groups:
        likelihood_index = group["medianScore"] - 1
        impact = group["tvlImpact"]
        if impact == 0:
            impact = 1
        impact_index = 5 - impact

        if data_matrix[impact_index][likelihood_index] == "":
            data_matrix[impact_index][likelihood_index] = [group["label"]]
        else:
            data_matrix[impact_index][likelihood_index].append(group["label"])

    return data_matrix

def median(values):
    if not values:
        return 0
    
    values.sort()
    middle = len(values) // 2
    
    if len(values) % 2 == 1:
        return values[middle]
    else:
        return (values[middle - 1] + values[middle]) / 2.0

def get_impact_score(impact, likelihood):
    scores = [
        [1, 1, 2, 2, 2],
        [0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1]
    ]
    
    if impact == 0:
        impact = 1
    
    impact_index = len(scores) - impact
    likelihood_index = likelihood - 1
    score = scores[impact_index][likelihood_index]
    
    return score

def current_timestamp():
    return int(time.time() * 1000)

def get_longevity_score(days):
    """
    5: Worst Score, new code, did not go to ape tax before
    4: Code has been live less than a month
    3: 1 to <4 months live
    2: 4+ months live
    1: Best score, Has had 8+ months live in prod with no critical issues found and No changes in code base
    """
    if days < 7:
        return 5
    if days <= 30:
        return 4
    if days < 120:
        return 3
    if days <= 240:
        return 2
    return 1

def get_tvl_impact(tvl):
    if tvl == 0:
        return 0
    if tvl < 1_000_000:
        return 1
    if tvl < 10_000_000:
        return 2
    if tvl < 50_000_000:
        return 3
    if tvl < 100_000_000:
        return 4
    return 5