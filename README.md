# crypto495
A mini crypto api built with Flask. Deployed via Serverless to AWS Lambda.


---
#### `/cryptos` GET
Get list of supported cryptos.
- `filter`: Filter text to search against crypto name and slug fields.
---
#### `/cryptos/{id}` GET
Get details of crypto by a given id.

---
#### `/cryptos/{id}/tokens`
Get all cryptos that are tokens of a single crypto by a given id.

---
#### `/categories` GET
Get all cryptos categorized by coin or token.
- `type`: [coin|token] to get one a single categorization.

