from prometheus_client import start_http_server, Gauge
import time
import xml.etree.ElementTree as ET
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create Prometheus metric for demonstration (assuming you have numeric values to monitor)
numeric_metric = Gauge('completeness', 'A sample numeric metric from JSON')

# Function to parse XML and convert it to JSON
def xml_to_json(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Convert XML data to a dictionary
        xml_data = {}
        for element in root:
            xml_data[element.tag] = element.text

        # Convert dictionary to JSON
        json_data = json.dumps(xml_data)
        return json_data
    except Exception as e:
        logging.error(f"Error parsing XML: {e}")
        return None

# Specify the path to your XML file
xml_file_path = '/var/lib/jenkins/workspace/Math/cppcheck-results.xml'

# Start Prometheus HTTP server
start_http_server(8000)  # Expose metrics on port 8000
logging.info("Prometheus HTTP server started on port 8000")

while True:
    json_data = xml_to_json(xml_file_path)
    if json_data is not None:
        # Log the JSON data (Prometheus doesn't handle raw JSON)
        logging.info(f"JSON data: {json_data}")

        # Assuming you have numeric data in your JSON, extract and use it
        # This is just a placeholder example
        data_dict = json.loads(json_data)
        numeric_value = data_dict.get('numeric_key')  # Replace 'numeric_key' with your actual key
        if numeric_value and isinstance(numeric_value, (int, float)):
            numeric_metric.set(numeric_value)
        else:
            logging.warning("Numeric value is missing or not a number")

    else:
        logging.error("Failed to process XML to JSON")

    time.sleep(100)  # Sleep for 10 seconds before next iteration

