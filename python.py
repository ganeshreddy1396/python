from prometheus_client import start_http_server, Gauge
import time
import xml.etree.ElementTree as ET

# Create Prometheus metric
metric = Gauge('python', 'metrics')

# Function to parse XML and extract the desired value
def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Modify this to extract the desired value from the XML
        parsed_value = float(root.find('your_xml_element').text)
        return parsed_value
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

# Specify the path to your Jenkins XML file
jenkins_xml_file_path = 'http://35.170.245.42:8080/job/Math/10/execution/node/3/ws/cppcheck-results.xml'

# Start Prometheus HTTP server
start_http_server(8000)  # Expose metrics on port 8000
while True:
    parsed_value = parse_xml(jenkins_xml_file_path)
    if parsed_value is not None:
        metric.set(parsed_value)
    time.sleep(1)

