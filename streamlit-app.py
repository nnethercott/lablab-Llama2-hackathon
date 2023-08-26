from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
import streamlit as st
from PIL import Image
import pandas as pd

st.title("BLIP2 | Llama2 project")

# clarifai api key for model access
key = st.secrets['CLARIFAI_API_KEY']


# file uploader
file_data = st.file_uploader("Upload Image", type=['jpg', 'png'])
if file_data == None:
    st.warning("File needs to be uploaded")
    st.stop()
else:
    image = Image.open(file_data)
    st.image(image)


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
                        base64=file_data.getvalue()
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
st.markdown(body=f'### {results.outputs[0].data.text.raw}')
