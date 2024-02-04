from prometheus_client import start_http_server, Gauge
import time
import xml.etree.ElementTree as ET
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
logging.info(f"Prometheus server started on port 8000")

while True:
    logging.debug(f"Reading XML file from {jenkins_xml_file_path}")
    json_data = xml_to_json(jenkins_xml_file_path)
    
    if json_data is not None:
        logging.debug(f"Received JSON data: {json_data}")
        
        # Convert JSON string back to dictionary
        data_dict = json.loads(json_data)

        # Extract values and update Prometheus metrics
        build_number = data_dict.get('build_number')
        duration = data_dict.get('duration')
        
        if build_number is not None and isinstance(build_number, (int, float)):
            build_number_metric.set(build_number)
            logging.debug(f"Updated build_number_metric: {build_number}")
        else:
            logging.warning(f"Invalid or missing build_number: {build_number}")

        if duration is not None and isinstance(duration, (int, float)):
            duration_metric.set(duration)
            logging.debug(f"Updated duration_metric: {duration}")
        else:
            logging.warning(f"Invalid or missing duration: {duration}")

    else:
        logging.error("Failed to process JSON data")
    
    time.sleep(10000)