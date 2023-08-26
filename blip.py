
##############################################################################
# In this section, we set the user authentication, app ID, workflow ID, and
# image URL. Change these strings to run your own example.
##############################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
import streamlit as st

PAT = st.secrets.PAT
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = st.secrets.USER_ID
APP_ID = st.secrets.APP_ID
# Change these to whatever model and text URL you want to use
WORKFLOW_ID = 'extract-visual-queues'

##########################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
##########################################################################


def extract_visual_queues(image_bytes):
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
                            base64=image_bytes
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

    return results.outputs[-1].data.text.raw
