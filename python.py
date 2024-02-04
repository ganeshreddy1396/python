
from prometheus_client import start_http_server, Gauge
import time
import xml.etree.ElementTree as ET
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create Prometheus metrics
build_number_metric = Gauge('jenkins_build_number', 'Jenkins build number')
duration_metric = Gauge('jenkins_build_duration', 'Duration of Jenkins build')

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

# Specify the path to your Jenkins XML file
jenkins_xml_file_path = '/var/lib/jenkins/workspace/Math/cppcheck-results.xml'

# Start Prometheus HTTP server
start_http_server(8000)  # Expose metrics on port 8000

while True:
    json_data = xml_to_json(jenkins_xml_file_path)
    if json_data is not None:
        # Convert JSON string back to dictionary
        data_dict = json.loads(json_data)

        # Extract values and update Prometheus metrics
        build_number = data_dict.get('build_number')
        if build_number is not None:
            build_number_metric.set(build_number)

        duration = data_dict.get('duration')
        if duration is not None:
            duration_metric.set(duration)

        logging.info("JSON data processed successfully: Build Number - {}, Duration - {}".format(build_number, duration))
    else:
        logging.error("Failed to process JSON data")
    time.sleep(10000)


