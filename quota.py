import requests
import csv

# Prompt the user for the Isilon FQDN, username, and password
isilon_fqdn = input("Enter the Isilon FQDN: ")
isilon_username = input("Enter the Isilon username: ")
isilon_password = input("Enter the Isilon password: ")

# Set the OneFS API endpoint and headers
onefs_endpoint = f"https://{isilon_fqdn}:8080"
onefs_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Send a GET request to retrieve the quotas with the credentials and headers
quotas_endpoint = f"{onefs_endpoint}/platform/1/quota/quotas"
quotas_response = requests.get(quotas_endpoint, auth=(isilon_username, isilon_password), headers=onefs_headers)

# Check if the request was successful
if quotas_response.status_code == 200:
    # Get the quotas from the response JSON
    quotas = quotas_response.json()

    # Loop through the quotas and check if they need to be expanded
    for quota in quotas["quotas"]:
        # Extract the current usage, current quota, and quota path from the quota
        current_usage_bytes = int(quota["usage"]["physical"]["total_bytes"])
        current_quota_bytes = int(quota["thresholds"]["hard"]["physical"]["threshold"])
        quota_path = quota["path"]

        # Calculate the current usage as a percentage of the current quota
        current_usage_percent = current_usage_bytes / current_quota_bytes * 100

        # Check if the current usage is over 90%
        if current_usage_percent > 90:
            # Calculate the new quota as 105% of the current quota
            new_quota_bytes = int(current_quota_bytes * 1.05)

            # Set the new quota using a PUT request
            new_quota_endpoint = f"{onefs_endpoint}/platform/1/quota/quotas/{quota_path}"
            new_quota_data = {
                "thresholds": {
                    "hard": {
                        "physical": {
                            "threshold": new_quota_bytes
                        }
                    }
                }
            }
            new_quota_response = requests.put(new_quota_endpoint, auth=(isilon_username, isilon_password), headers=onefs_headers, json=new_quota_data)

            # Check if the new quota was set successfully
            if new_quota_response.status_code == 200:
                print(f"Quota expanded for {quota_path}.")
            else:
                print(f"Failed to expand quota for {quota_path}.")

    # Write the quota information to a CSV file
    with open("quota_info.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["File System", "Current Usage", "Current Quota"])
        for quota in quotas["quotas"]:
            current_usage_bytes = int(quota["usage"]["physical"]["total_bytes"])
            current_quota_bytes = int(quota["thresholds"]["hard"]["physical"]["threshold"])
            current_usage = "{:.2f} GB".format(current_usage_bytes / (1024 ** 3))
            current_quota = "{:.2f} GB".format(current_quota_bytes / (1024 ** 3))
