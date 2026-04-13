# Name of the resource that got created in GCP  when I ran this code was 
# reasoning_engine = vertexai.preview.reasoning_engines.ReasoningEngine('projects/453906697366/locations/us-east4/reasoningEngines/8347896898354413568'
import vertexai
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
import datetime
from zoneinfo import ZoneInfo

# 1. Configuration 
PROJECT_ID = "dataanalytics-013124-1d2"
LOCATION = "us-east4"
STAGING_BUCKET = "gs://theruzo"
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# 2. Define the Agent Structure
# Vertex AI requires a class-based structure for serialization (pickling)
class TimeAgentApp:
    def __init__(self, project: str, location: str):
        self.project_id = project
        self.location = location

    def set_up(self):
        """This runs on the server to initialize the agent."""
        # Use the 2026 stable model we discussed
        self.model = ChatVertexAI(model="gemini-2.5-flash")

        # Your  tool logic
        
        def get_current_time(location: str = "Fanwood, NJ"):
            """Returns the current time for an IANA Time Zone string (e.g. 'Europe/London')."""
            try:
                tz = ZoneInfo(location)
                now = datetime.datetime.now(tz)
                return f"The current time in {location} is {now.strftime('%H:%M:%S')}"
            except Exception:
                return f"Error: '{location}' not found. Use IANA format like 'Asia/Tokyo'."

        self.tools = [get_current_time]
        self.agent = create_react_agent(self.model, self.tools)

    def query(self, input_text: str):
        """The entry point for API calls."""
        inputs = {"messages": [("user", input_text)]}
        result = self.agent.invoke(inputs)
        return result["messages"][-1].content

# 3. Execution & Deployment
if __name__ == "__main__":
    print("🛠️  Testing agent locally...")
    local_app = TimeAgentApp(PROJECT_ID, LOCATION)
    local_app.set_up()
    print(f"Local Test: {local_app.query('What time is it in London?')}")

    print("\n🚀 Deploying to Vertex AI Agent Engine (this takes ~3-5 mins)...")
    remote_agent = reasoning_engines.ReasoningEngine.create(
        TimeAgentApp(PROJECT_ID, LOCATION),
        requirements=[
            "google-cloud-aiplatform[agent_engines,langchain]",
            "langchain-google-vertexai",
            "langgraph",
            "tzdata", # Required for IANA zone data on Linux/WSL
            "cloudpickle==3.0.0" 
        ],
        display_name="Time_Zone_Agent_2026",
    )

    print(f"\n✅ Deployment Complete!")
    print(f"Resource Name: {remote_agent.resource_name}")
