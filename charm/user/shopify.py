import json
import requests

def send_shopify(newsletter, first_name, last_name, email, telephone, address, city, country, postalCode, username, birthdate):
    url = "https://pharmaziegasse-kosmetik.myshopify.com/admin/api/2019-10/graphql.json"

    query = """
    mutation($input: CustomerInput!) {
        customerCreate(input: $input) {
            customer {
                id
                firstName
                lastName
                email
                phone
            }
            userErrors {
                field
                message
            }
        }
    }
    """

    variables = {
        "input": {
            "acceptsMarketing": newsletter,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "phone": telephone,
            "addresses": [{
                "address1": address,
                "city": city,
                "country": country,
                "firstName": first_name,
                "lastName": last_name,
                "phone": telephone,
                "zip": postalCode
            }],
            "metafields": [
                {
                "description": "Customer's Birthdate",
                "key": "birthdate",
                "namespace": "default_custom_field",
                "value": "",
                "valueType": "STRING"
                },
                {
                "description": "Unique User Identifier",
                "key": "uid",
                "namespace": "default_custom_field",
                "value": username,
                "valueType": "STRING"
                }
            ]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": "28648897ba36c9c819b4517c1d397eeb"
    }

    r = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    print(r.status_code)
    print(r.text)

    jsondata = r.text
    data = json.loads(jsondata)

    return(data['data']['customerCreate']['customer']['id'])