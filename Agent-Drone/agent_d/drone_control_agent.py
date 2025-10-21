from string import Template
import requests
from dotenv import load_dotenv
import os
import json


from agent_d.skills import (
    takeoff, land, fly_to_coordinates, circle_a_point,
    follow_me, return_to_launch, rotate_to_specific_yaw, hover_at_location
)
from agent_d.utils.helper_functions import example_helper
from agent_d.utils.prompts import LLM_PROMPTS

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class DroneControlAgent:
    def __init__(self):
        user_ltm = self.__get_ltm()
        system_message = LLM_PROMPTS["DRONE_AGENT_PROMPT"]

        if user_ltm:
            user_ltm = "\n" + user_ltm
            system_message = Template(system_message).substitute(basic_user_information=user_ltm)
        
        self.system_message = system_message
        self.api_key = GEMINI_API_KEY
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.tools = self.__get_tools()

    def __get_ltm(self):
        return None

    def __get_tools(self):
        return {
            "function_declarations": [
                {
                    "name": "takeoff",
                    "description": "Take off the drone to a specified height.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "height": {
                                "type": "number",
                                "description": "The height to take off to in meters."
                            }
                        },
                        "required": ["height"]
                    }
                },
                {
                    "name": "land",
                    "description": "Land the drone safely."
                },
                {
                    "name": "fly_to_coordinates",
                    "description": "Fly the drone to specified coordinates.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "X coordinate"},
                            "y": {"type": "number", "description": "Y coordinate"},
                            "z": {"type": "number", "description": "Z coordinate"}
                        },
                        "required": ["x", "y", "z"]
                    }
                },
                {
                    "name": "circle_a_point",
                    "description": "Circle the drone around a point.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "radius": {"type": "number", "description": "Radius of the circle"},
                            "x_center": {"type": "number", "description": "X center"},
                            "y_center": {"type": "number", "description": "Y center"},
                            "altitude": {"type": "number", "description": "Altitude"}
                        },
                        "required": ["radius", "x_center", "y_center", "altitude"]
                    }
                },
                {
                    "name": "follow_me",
                    "description": "Make the drone follow a target.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number", "description": "Latitude"},
                            "longitude": {"type": "number", "description": "Longitude"},
                            "altitude": {"type": "number", "description": "Altitude"},
                            "velocity": {"type": "number", "description": "Velocity"}
                        },
                        "required": ["latitude", "longitude", "altitude", "velocity"]
                    }
                },
                {
                    "name": "return_to_launch",
                    "description": "Return the drone to launch point."
                },
                {
                    "name": "rotate_to_specific_yaw",
                    "description": "Rotate the drone to a specific yaw.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "yaw": {"type": "number", "description": "Yaw angle in degrees"}
                        },
                        "required": ["yaw"]
                    }
                },
                {
                    "name": "hover_at_location",
                    "description": "Hover the drone at a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "X coordinate"},
                            "y": {"type": "number", "description": "Y coordinate"},
                            "z": {"type": "number", "description": "Z coordinate"}
                        },
                        "required": ["x", "y", "z"]
                    }
                }
            ]
        }

    async def run_conversation(self):
        while True:
            try:
                user_input = input("Enter your command: ")
                if user_input.lower() == "exit":
                    break
                response = self.__call_gemini(user_input)
                await self.__handle_response(response)
            except EOFError:
                print("Input interrupted. Exiting.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    def __call_gemini(self, user_input):
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": user_input
                        }
                    ]
                }
            ],
            "system_instruction": {
                "parts": [
                    {
                        "text": self.system_message
                    }
                ]
            },
            "tools": [self.tools]
        }
        resp = requests.post(self.url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print(f"API Error: {resp.status_code} - {resp.text}")
            return {}
        response_json = resp.json()
        print(f"API Response: {response_json}")  # Debug print
        return response_json

    async def __handle_response(self, response):
        if 'candidates' in response:
            for candidate in response['candidates']:
                if 'content' in candidate:
                    for part in candidate['content']['parts']:
                        if 'functionCall' in part:
                            await self.__call_function(part['functionCall'])
                        elif 'text' in part:
                            print(part['text'])

    async def __call_function(self, function_call):
        name = function_call['name']
        args = function_call.get('args', {})
        if name == "takeoff":
            await takeoff.takeoff(**args)
        elif name == "land":
            await land.land()
        elif name == "fly_to_coordinates":
            await fly_to_coordinates.fly_to(**args)
        elif name == "circle_a_point":
            await circle_a_point.circle_a_point(**args)
        elif name == "follow_me":
            await follow_me.follow_me(**args)
        elif name == "return_to_launch":
            await return_to_launch.return_to_launch()
        elif name == "rotate_to_specific_yaw":
            await rotate_to_specific_yaw.rotate_to_yaw(**args)
        elif name == "hover_at_location":
            await hover_at_location.hover_at_location(**args)
        print(f"Executed {name}")