import vertexai
from vertexai import agent_engines
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from zoneinfo import ZoneInfo
import datetime

# Initialize GCP Environment
PROJECT_ID = "dataanalytics-013124-1d2"
LOCATION = "us-east4"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# 1. Define a Tool (Standard Python function)
def get_current_time(location: str = "Fanwood, NJ"):
    """
    Returns the current time for a given location.
    The 'location' parameter must be an IANA Time Zone string 
    (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo').
    Defaults to Fanwood, NJ.
    """
    try:
        # Use the location string directly as the TimeZone ID
        tz = ZoneInfo(location)
        now = datetime.datetime.now(tz)
        return f"The current time in {location} is {now.strftime('%H:%M:%S')}"
    except Exception as e:
        return f"Error: Could not find timezone for '{location}'. Please use IANA format like 'America/New_York'."

# Use this in your tools list
tools = [get_current_time]

# 2. Initialize the "Brain" (Gemini 2.5 Flash)
model = ChatVertexAI(model="gemini-2.5-flash")

# 3. Create the LangGraph Agent
# The 'create_react_agent' is a prebuilt graph that handles the 
# "Thought -> Action -> Observation" loop for you.
agent_graph = create_react_agent(model, tools)

# 4. Local Test
inputs = {"messages": [("user", "What time is it in Paris?")]}
for chunk in agent_graph.stream(inputs, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
