from dotenv import load_dotenv
import os
import time
import json
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

def main():

    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        credential = CognitiveServicesCredentials(cog_key) 
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Use report1.jpg for analysis
        image_file = r'C:\files\PoC\report1.jpg'
        read_results = GetTextRead(image_file)

        # If the operation was successfully, process the text line by line
        if read_results.status == OperationStatusCodes.succeeded:
            lines_text = []
            for page in read_results.analyze_result.read_results:
                for line in page.lines:
                    lines_text.append(line.text)

            # Convert list to JSON and write to a file
            with open('result.json', 'w') as f:
                json.dump(lines_text, f)

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('Reading text in {}\n'.format(image_file))
    with open(image_file, mode="rb") as image_data:
        read_op = cv_client.read_in_stream(image_data, raw=True)

    # Get the async operation ID so we can check for the results
    operation_location = read_op.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the asynchronous operation to complete
    while True:
        read_results = cv_client.get_read_result(operation_id)
        if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    # Return the read results
    return read_results

if __name__ == "__main__":
    main()