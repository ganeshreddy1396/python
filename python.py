import xml.etree.ElementTree as ET
from prometheus_client import start_http_server, Gauge
import time

# Specify the path to your XML file
xml_file_path = '/var/lib/jenkins/workspace/Math/cppcheck-results.xml'

# Create a Prometheus Gauge metric
metric = Gauge('completeness', 'percentage of static code analyzed in code')

while True:
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Assuming you want to extract a specific element from the XML
        for child in root:
            for grand_c in child:
                parsed_value = grand_c.text
                break  # Assuming you only need the first value

        # Ensure that parsed_value contains valid data
        if parsed_value:
            parsed_value = parsed_value[-10:]  # Adjust the slicing as needed

            # Set the metric value
            metric.set(float(parsed_value))
            print(f'Parsed Value: {parsed_value}')

    except Exception as e:
        print(f'Error: {str(e)}')

    # Sleep for a while before checking the XML file again (adjust the sleep time as needed)
    time.sleep(1000)

# Start the Prometheus HTTP server (this should be outside the loop)
start_http_server(8000)  # 9090 is the Prometheus server port
