##############################################################################
# SIDE .PY SCRIPT FOR ME TO TEST STUFF WITHOUT THE STREAMLIT APP
##############################################################################

from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from io import BytesIO
import base64
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# load image locally
with open('/Users/nathanielnethercott/Desktop/nate_small.png', "rb") as f:
    file_bytes = f.read()


##############################################################################
# In this section, we set the user authentication, app ID, workflow ID, and
# image URL. Change these strings to run your own example.
##############################################################################

USER_ID = 'nnethercott'
# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '038384abf99b4608be359d56f21918cc'
APP_ID = 'BLIP2_Llama2'
# Change these to make your own predictions
WORKFLOW_ID = 'image-to-text-blip'

##########################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
##########################################################################


channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

# The userDataObject is required when using a PAT
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

post_workflow_results_response = stub.PostWorkflowResults(
    service_pb2.PostWorkflowResultsRequest(
        user_app_id=userDataObject,
        workflow_id=WORKFLOW_ID,
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
    print(post_workflow_results_response.status)
    raise Exception("Post workflow results failed, status: " +
                    post_workflow_results_response.status.description)

# We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
results = post_workflow_results_response.results[0]

# Uncomment this line to print the full Response JSON
print(results.outputs[0].data.text.raw)
