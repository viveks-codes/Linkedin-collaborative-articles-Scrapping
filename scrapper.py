import string
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service()
driver = webdriver.Edge(service=service)

# List of alphabets from A to Z
alphabets = string.ascii_lowercase

# LinkedIn topics page base URL
base_url = "https://www.linkedin.com/pulse/topics/browse/"

# Initialize lists to store topic data
all_topic_data = []

# Extract topics for each alphabet
for alphabet in alphabets:
    # Construct the URL for the specific alphabet
    url = base_url + alphabet
    driver.get(url)

    # Find all links on the page
    links = driver.find_elements(By.TAG_NAME, 'a')

    # Extract URLs from links
    all_links = [link.get_attribute('href') for link in links]

    # Filter the links using regex
    filtered_links = [link for link in all_links if re.search(r'/topics/.+', link)]

    # Extract topic names and URLs
    topic_data = [{"name": re.search(r'/topics/(.+?)/?', link).group(1), "link": link} for link in filtered_links]

    # Add topic data to the list
    all_topic_data.extend(topic_data)

# Close the WebDriver session
driver.quit()

# Create DataFrame from the topic data
df = pd.DataFrame(all_topic_data)

# Save DataFrame to CSV file
df.to_csv("linkedin_topics.csv", index=False)

print("CSV file created successfully.")
