import vertexai
from vertexai.preview import reasoning_engines

PROJECT_ID = "dataanalytics-013124-1d2"
LOCATION = "us-east4"
vertexai.init(project=PROJECT_ID, location=LOCATION)

remote_agent = reasoning_engines.ReasoningEngine("projects/453906697366/locations/us-east4/reasoningEngines/8347896898354413568")
print(remote_agent.query(input_text="What time is it in Tokyo?"))
print(remote_agent.query(input_text="What time is it in Paris?"))
print(remote_agent.query(input_text="What time is it?")) 
