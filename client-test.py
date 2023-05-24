from algoliasearch.search_client import SearchClient

key = input("Enter your secure key:")
print(key)

# Connect and authenticate with your Algolia app
client = SearchClient.create("OKF83BFQS4", key)

# Create a new index and add a record
index = client.init_index("multi-tenant-demo")

# Search the index and print the results
results = index.search("phone")
print(results["hits"][0])
