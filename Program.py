
from azure.cognitiveservices.vision.computervision import ComputerVisionClient as visionsdk
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import ImageAnalysisResult, VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

key = "518b99159bbb4b61b36b0091001a767a"
endpoint = "https://cs1-3600097.cognitiveservices.azure.com/"

def AnalyzeImage (endpoint:str, key: str) ->None:

    service_options = visionsdk.VisionServiceOptions(endpoint, key)

    ''' Specify the image file on disk to analyze. sample.jpg is a good example to show most features'''
    vision_source = visionsdk.VisionSource(filename=r"sample.jpg")

    analysis_options = visionsdk.ImageAnalysisOptions()

    analysis_options.features = (
        '''point 2 
            write your code here'''
    )

    image_analyzer = visionsdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    print(" Please wait for image analysis results...")

    result = image_analyzer.analyze()

    # Checks result.
    if result.reason == visionsdk.ImageAnalysisResultReason.ANALYZED:
        if result.objects is not None:
            print(" Objects:")
            for object in result.objects:
                print(f"   {object.name}")

        if result.tags is not None:
            print(" Tags:")
            for tag in result.tags:
                '''point 3 
                   write your code here'''
                print(f"   {tag.name} with confidence {tag.confidence}")

        if result.people is not None:
            print(" People:")
            for person in result.people:
                '''point 4 
                   write your code here'''

        if result.text is not None:
            print(" Text:")
            for line in result.text.lines:
                '''point 5 
                   write your code here'''

    else:

        error_details = visionsdk.ImageAnalysisErrorDetails.from_result(result)
        print(" Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))
        print(" Did you set the computer vision endpoint and key?")



AnalyzeImage (endpoint,key)


