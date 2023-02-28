# Quota Expansion Tool for Isilon

This Python script uses the OneFS API to expand quotas for file systems on an Isilon storage system. It prompts the user for the Isilon FQDN, username, and password, sends a GET request to retrieve the quotas, and then loops through the quotas to check if they need to be expanded. If a quota needs to be expanded, the script calculates a new quota as 105% of the current quota and then sends a PUT request to set the new quota. Finally, the script writes the quota information to a CSV file.
