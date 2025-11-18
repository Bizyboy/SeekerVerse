# ai_server.py
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json
import os
from openai import OpenAI

# --- Configuration ---
# Initialize the OpenAI client. The API key and base URL are automatically
# configured from the environment variables in the sandbox.
try:
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    # Fallback to a mock client if the real one fails
    class MockOpenAI:
        def chat(self):
            return self
        def completions(self):
            return self
        def create(self, **kwargs):
            # Simple mock response structure
            return type('MockResponse', (object,), {
                'choices': [type('MockChoice', (object,), {
                    'message': type('MockMessage', (object,), {
                        'content': json.dumps({
                            "dialogue": "I sense a great disturbance in the Coherence. Perhaps you should seek the ancient ruins to restore your balance.",
                            "action": "MOVE_TO_RUINS"
                        })
                    })
                })]
            })()
    client = MockOpenAI()
    print("Using Mock OpenAI Client.")

app = FastAPI(
    title="SeekerVerse AI Bridge",
    description="API for integrating game context with Large Language Models for dynamic NPC interactions."
)

# --- Data Models ---

class GameContext(BaseModel):
    """Data model for the context sent from the game client."""
    player_id: str = Field(..., description="Unique identifier for the player.")
    location: str = Field(..., description="Current in-game location (e.g., 'The Nexus', 'Ancient Ruins').")
    inventory: List[str] = Field(default_factory=list, description="List of key items in the player's inventory.")
    last_action: str = Field(..., description="The player's last significant action.")
    query: str = Field(..., description="The player's natural language query or input to the NPC.")

class LLMResponse(BaseModel):
    """Data model for the structured response expected from the LLM."""
    dialogue: str = Field(..., description="The NPC's natural language response to the player.")
    action: str = Field(..., description="A structured action command for the game engine (e.g., 'TRADE_OFFER', 'GIVE_QUEST', 'NO_ACTION').")

# --- Mock Implementations ---

class MockVectorDB:
    """A mock class to simulate context retrieval from a Vector Database."""
    def query(self, player_query: str, location: str) -> str:
        """Simulates querying the Vector DB for relevant NPC memories."""
        if "ruins" in location.lower():
            return "The Guardian remembers the prophecy of the 'Shattered Seed' and the need for a 'Master Seeker' to restore the PCG graph."
        elif "trade" in player_query.lower() or "lumen" in player_query.lower():
            return "The Guardian has a hidden memory of a rare 'Clarity Shard' that can be exchanged for 500 Lumen."
        else:
            return "The Guardian's memory is blank on this topic, focusing only on the current location's general state."

vector_db = MockVectorDB()

# --- API Endpoint ---

@app.post("/npc/interact", response_model=LLMResponse, tags=["NPC Interaction"])
async def generate_npc_response(ctx: GameContext):
    """
    Generates a structured NPC response based on game context and LLM processing.
    """
    # 1. Retrieve NPC memory from Vector DB
    memories = vector_db.query(ctx.query, ctx.location)
    
    # 2. Construct System Prompt for the LLM
    system_prompt = f"""
    You are a cryptic and wise Guardian of the SeekerVerse. Your goal is to guide the player
    using your knowledge and the provided context, always responding in the specified JSON format.
    
    **Persona & Context:**
    - Location: {ctx.location}
    - Player Inventory: {', '.join(ctx.inventory) if ctx.inventory else 'None'}
    - Last Player Action: {ctx.last_action}
    - Relevant NPC Memories: {memories}
    - Current Economy State: Inflation High.

    **Instructions:**
    1. Respond to the player's query: "{ctx.query}".
    2. Your response must be a single JSON object matching the structure: {{"dialogue": "...", "action": "..."}}.
    3. The 'action' field must be a capitalized, underscore-separated command (e.g., 'GIVE_QUEST', 'TRADE_OFFER', 'NO_ACTION').
    4. Base your dialogue and action on the provided context and memories.
    """
    
    # 3. Call LLM
    try:
        completion = client.chat.completions.create(
            model="gemini-2.5-flash", # Using a fast, capable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": ctx.query}
            ],
            response_format={"type": "json_object"}
        )
        
        # 4. Parse and Validate LLM Response
        llm_output = completion.choices[0].message.content
        response_data = json.loads(llm_output)
        
        # Validate against the Pydantic model
        return LLMResponse(**response_data)

    except Exception as e:
        # Fallback for LLM failure or JSON parsing error
        print(f"LLM or JSON parsing error: {e}")
        return LLMResponse(
            dialogue="The threads of fate are tangled. I cannot perceive your meaning right now. Try again.",
            action="ERROR_LLM_FAILURE"
        )

# Example usage (for local testing):
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
