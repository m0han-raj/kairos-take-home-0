from agent_host.agent import run_agent
import sys
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    query = input("enter what research paper you want to search: ")
    run_agent(query)