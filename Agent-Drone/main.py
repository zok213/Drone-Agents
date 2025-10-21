import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from agent_d.drone_control_agent import DroneControlAgent

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("Gemini API key not found. Please set it in the .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def main():
    # Initialize the DroneControlAgent
    agent = DroneControlAgent()
    
    # Run the conversation
    asyncio.run(agent.run_conversation())

if __name__ == "__main__":
    main()
