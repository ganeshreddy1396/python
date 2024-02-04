from prometheus_client import start_http_server, Gauge
import time
import xml.etree.ElementTree as ET
import json

# Create Prometheus metric
metric = Gauge('jenkins_xml_to_json', 'XML Data Converted to JSON')

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
        print(f"Error parsing XML: {e}")
        return None

# Specify the path to your Jenkins XML file
jenkins_xml_file_path = '/var/lib/jenkins/workspace/Math/cppcheck-results.xml'

# Start Prometheus HTTP server
start_http_server(8000)  # Expose metrics on port 8000

while True:
    json_data = xml_to_json(jenkins_xml_file_path)
    if json_data is not None:
        # Here you should handle the conversion of json_data to a numeric value if necessary
        # metric.set(converted_value)
        pass
    time.sleep(10000)
