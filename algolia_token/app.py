import json
import os
import requests
import time
from algoliasearch.search_client import SearchClient

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    body = json.loads(event["body"])
    filter_attribute = os.environ["ALGOLIA_KEY_FILTER_ATTRIBUTE"]
    duration = int(os.environ["ALGOLIA_KEY_DURATION"])
    indices = os.environ["ALGOLIA_KEY_INDICES"]

    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

        raise e

    valid_until = int(time.time()) + duration
    public_key = SearchClient.generate_secured_api_key(
        os.environ["ALGOLIA_API_SEARCH_KEY"],
        {
            "validUntil": valid_until,
            "restrictIndices": indices,
            "filters": f"{filter_attribute}:{body['Id']}"
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": ip.text.replace("\n", ""),
            "id": body["Id"],
            "searchKey": public_key
        }),
    }
