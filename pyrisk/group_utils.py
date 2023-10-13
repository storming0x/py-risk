import requests
import diskcache as dc
from typing import Dict
from rich.text import Text
from pyrisk.utils import get_or_create_cli_dir_path, current_timestamp

cli_directory = get_or_create_cli_dir_path()
# Create a disk-based cache on users home directory
cache_group = dc.Cache(cli_directory, expire=600)


# Dev note: currently using ydaemon API.
# Plan to migrate to subgraph + onchain contracts for v3 support soon
def get_vaults_data(chainId: int, force_refresh=False):
    if force_refresh:
        # If force_refresh is True, clear the cache
        cache_group.clear()

    # Check if the data is in the cache
    cache_key = str(chainId)  # Convert the chainId to a string for the cache key
    if cache_key in cache_group:
        return cache_group[cache_key]

    # If not in cache, fetch the data
    url = f"https://ydaemon.yearn.fi/{chainId}/vaults/all?classification=all&strategiesDetails=withDetails"
    response = requests.get(url)
    risk_data = response.json()

    # Store the data in the cache to expire in 10 minutes
    cache_group.set(cache_key, risk_data, expire=600)

    return risk_data


# Function to process data and group into risk groups
def map_risk_group_data(data):
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
                        "auditScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("auditScore", 0),
                        "codeReviewScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("codeReviewScore", 0),
                        "testingScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("testingScore", 0),
                        "protocolSafetyScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("protocolSafetyScore", 0),
                        "complexityScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("complexityScore", 0),
                        "teamKnowledgeScore": strategy.get("risk", {})
                        .get("riskDetails", {})
                        .get("teamKnowledgeScore", 0),
                    }

                currentTVL = (
                    strategy.get("risk", {}).get("allocation", {}).get("currentTVL", 0)
                )
                status_color = (
                    strategy.get("risk", {})
                    .get("allocation", {})
                    .get("status", "green")
                )
                # DEV: sanity check. all currentTVL aggregate from each strategies in the risk group should be the same
                if currentTVL > risk_groups[risk_group]["tvl"]:
                    risk_groups[risk_group]["tvl"] = currentTVL
                risk_groups[risk_group]["strategiesCount"] += 1
                risk_groups[risk_group]["strategies"].append(strategy)
                risk_groups[risk_group]["status"] = status_color

                activation = strategy.get("details", {}).get("activation", 0)
                if (
                    not risk_groups[risk_group]["oldestActivation"]
                    or activation < risk_groups[risk_group]["oldestActivation"]
                ):
                    risk_groups[risk_group]["oldestActivation"] = activation

    for risk_group in risk_groups.values():
        risk_group["longevityScore"] = (
            5
            if not risk_group["strategies"]
            else get_longevity_score(
                (current_timestamp() - risk_group["oldestActivation"]) / 86400
            )
        )
        risk_group["medianScore"] = median(
            [
                risk_group["auditScore"],
                risk_group["codeReviewScore"],
                risk_group["testingScore"],
                risk_group["protocolSafetyScore"],
                risk_group["complexityScore"],
                risk_group["teamKnowledgeScore"],
                risk_group["longevityScore"],
            ]
        )
        risk_group["tvlImpact"] = get_tvl_impact(risk_group["tvl"])
        risk_group["impactScore"] = get_impact_score(
            risk_group["tvlImpact"], risk_group["medianScore"]
        )

    return risk_groups


def get_risk_group_data(chainId: int, force_refresh=False):
    # Get vaults data
    vaults_data = get_vaults_data(chainId, force_refresh)

    # Process data and group into risk groups
    risk_group_data = map_risk_group_data(vaults_data)

    return risk_group_data


def create_data_matrix(groups: Dict):
    data_matrix = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
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


def get_impact_score(impact: int, likelihood: int):
    scores = [
        [1, 1, 2, 2, 2],
        [0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ]

    if impact == 0:
        impact = 1

    impact_index = len(scores) - impact
    likelihood_index = likelihood - 1
    score = scores[impact_index][likelihood_index]

    return score


def get_longevity_score(days: int):
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


def get_tvl_impact(tvl: float):
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


def format_score(score: int):
    style = "white"
    if score == 0:
        return "N/A"
    if score == 1:
        style = "green"
    if score == 2 or score == 3:
        style = "yellow"
    if score == 4 or score == 5:
        style = "red"

    return Text(str(score), style=style)
