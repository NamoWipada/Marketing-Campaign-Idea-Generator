# src/main.py
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from model import GeminiFlashCampaignGenerator
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests
import gradio as gr
import threading

executor = ThreadPoolExecutor()
app = FastAPI()
generator = GeminiFlashCampaignGenerator()

# ----------------------
# FastAPI models & endpoint
# ----------------------
class CampaignInput(BaseModel):
    industry: str
    campaign_objective: str
    target_audience: str
    budget_range: str
    channels_preference: List[str]
    mood_tone: str = ""  # Optional
    topic: str = ""      # Optional

@app.post("/generate")
async def generate_campaign(req: CampaignInput):
    parameters = req.dict()
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(executor, generator.generate_campaign, parameters)
        return {"input": parameters, "output": result}
    except Exception as e:
        return {"error": str(e)}

# ----------------------
# Gradio ChatGPT-style
# ----------------------
API_URL = "http://127.0.0.1:8000/generate"

def chat_with_ai(chat_history, industry, campaign_objective, target_audience,
                 budget_range, channels_preference, mood_tone, topic):
    payload = {
        "industry": industry,
        "campaign_objective": campaign_objective,
        "target_audience": target_audience,
        "budget_range": budget_range,
        "channels_preference": channels_preference,
        "mood_tone": mood_tone,
        "topic": topic
    }
    try:
        response = requests.post(API_URL, json=payload).json()
        ai_message = response.get("output", response.get("error", "No output"))
    except Exception as e:
        ai_message = f"Error: {str(e)}"
    
    chat_history.append(("User", f"{payload}"))
    chat_history.append(("AI", ai_message))
    return chat_history, ""

def start_gradio():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=1):
                industry = gr.Dropdown(
                    choices=["F&B", "Telecom", "Corporate", "Government", "Tech", "HR", "Finance", "Event"],
                    label="Industry"
                )
                campaign_objective = gr.Dropdown(
                    choices=["Awareness", "Conversion", "Lead Generation", "Brand Engagement", "Innovation"],
                    label="Campaign Objective"
                )
                target_audience = gr.Dropdown(
                    choices=["Gen Z","Millennials","Gen X","Baby Boomers","Working Professionals","Students",
                             "Stay-at-home","Entrepreneurs / Small Business Owners","Elderly / Retired"],
                    label="Target Audience"
                )
                budget_range = gr.Dropdown(
                    choices=["Low","Medium","High"], label="Budget Range"
                )
                channels_preference = gr.CheckboxGroup(
                    choices=["Digital","Social","Mobile","Metaverse","Event"],
                    label="Channels Preference"
                )
                mood_tone = gr.Textbox(label="Mood & Tone (optional)")
                topic = gr.Textbox(label="Topic (optional)")
                submit_btn = gr.Button("Send")

            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Campaign Chatbot").style(height=600)
                state = gr.State([])  # Chat history

        submit_btn.click(
            chat_with_ai,
            inputs=[state, industry, campaign_objective, target_audience,
                    budget_range, channels_preference, mood_tone, topic],
            outputs=[chatbot, state]
        )

    demo.launch(server_name="127.0.0.1", server_port=7860)

# ----------------------
# Run FastAPI + Gradio
# ----------------------
if __name__ == "__main__":
    threading.Thread(target=start_gradio, daemon=True).start()
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)





# Note
# src/main.py
# from typing import List
# from fastapi import FastAPI
# from pydantic import BaseModel
# from model import GeminiFlashCampaignGenerator

# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# executor = ThreadPoolExecutor()

# app = FastAPI()
# generator = GeminiFlashCampaignGenerator()

# class CampaignInput(BaseModel):
#     industry: str
#     campaign_objective: str
#     target_audience: str
#     budget_range: str
#     channels_preference: List[str]
#     mood_tone: str = ""  # Optional
#     topic: str = ""      # Optional

# class UserRequest(BaseModel):
#     prompt: str

# @app.post("/generate")
# async def generate_campaign(req: CampaignInput):
#     parameters = req.dict()
#     loop = asyncio.get_event_loop()
#     try:
#         result = await loop.run_in_executor(executor, generator.generate_campaign, parameters)
#         return {
#             "input": parameters,
#             "output": result
#         }
#     except Exception as e:
        return {"error": str(e)}