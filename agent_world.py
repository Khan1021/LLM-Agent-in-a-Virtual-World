import os 
import re
from groq import Groq


class GridWorld:
    def __init__(self):
        #defining a 5x5 grid
        self.agent_pos=[0,0]    #bot starts in top left
        self.target_pos=[3,3]   #target is in the middle of the grid
        self.moves_taken=0


    def get_observation_text(self):
        """Translating grid state into a clearer text state with memory for the AI."""
        x, y = self.agent_pos
        tx, ty = self.target_pos
        
        # Calculate exactly which directions are physically blocked by walls
        blocked_moves = []
        if y == 0: blocked_moves.append("MOVE_UP")
        if y == 4: blocked_moves.append("MOVE_DOWN")
        if x == 0: blocked_moves.append("MOVE_LEFT")
        if x == 4: blocked_moves.append("MOVE_RIGHT")
        
        blocked_text = ", ".join(blocked_moves) if blocked_moves else "None"

        return (
            f"You are an autonomous robot routing agent in a 5x5 grid map.\n"
            f"Your current coordinates (X, Y) are: [{x}, {y}]\n"
            f"The target objective coordinates are: [{tx}, {ty}]\n"
            f"CRITICAL MAP RULES:\n"
            f"- To change X (left/right): MOVE_RIGHT increases X, MOVE_LEFT decreases X.\n"
            f"- To change Y (up/down): MOVE_DOWN increases Y, MOVE_UP decreases Y.\n"
            f"- WALL WARNING: Do NOT choose any of these moves from your current spot because they are blocked by walls: [{blocked_text}].\n"
            f"Total moves used: {self.moves_taken}/20.\n"
            f"Choose exactly one move from the available list."
        )
    


    def step(self, action):
        """Executes the action and moves the robot, keeping it inside walls."""
        self.moves_taken+=1
        x,y=self.agent_pos

        if action == "MOVE_UP" and y>0:
            self.agent_pos[1]-=1
        elif action == "MOVE_DOWN" and y < 4:
            self.agent_pos[1] += 1
        elif action == "MOVE_LEFT" and x > 0:
            self.agent_pos[0] -= 1
        elif action == "MOVE_RIGHT" and x < 4:
            self.agent_pos[0] += 1
        else:
            print(f" Action {action} hit a wall or was invalid!")

        #check if we reached the target position
        return self.agent_pos== self.target_pos
    

def query_llm_for_action(observation_text):
    """Sends the current world state to the AI and extracts a valid movement command."""
    # Instantiating the client. It automatically pulls your token from the environment variable
    client = Groq()
    
    # This strict system prompt forces the AI to reply with only the bracketed command
    system_instruction = (
        "You are an autonomous robot routing agent. Your ultimate goal is to navigate to the target coordinates. "
        "Analyze your current coordinates against target coordinates and respond with EXACTLY one valid action word from the "
        "available list, wrapped in square brackets. Example: [MOVE_RIGHT]. Do not explain your reasoning."
    )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": observation_text}
        ],
        temperature=0.0 # Setting temperature to 0 keeps the AI deterministic and perfectly logical
    )
    
    ai_text_reply = response.choices[0].message.content.strip().upper()
    print(f"[LLM RAW RESPONSE]: {ai_text_reply}")
    
    # Extract the action out of the bracket container via regex, e.g., "[MOVE_UP]" -> "MOVE_UP"
    match = re.search(r'\[(MOVE_UP|MOVE_DOWN|MOVE_LEFT|MOVE_RIGHT)\]', ai_text_reply)
    if match:
        return match.group(1)
    
    # Fallback default if the AI accidentally ignores brackets or gives a messy string
    return "MOVE_RIGHT"


def main():
    """main control loop for our AI application"""
    world = GridWorld()
    game_over = False

    print("--- Game Started! The Autonomous LLM Agent is now in control ---")

    # Set a maximum cap of 20 moves so a hallucinating AI doesn't cost money in an infinite loop
    while not game_over and world.moves_taken < 20:
        # 1. Show the world text state
        current_state = world.get_observation_text()
        print(f"\n[STEP {world.moves_taken + 1}] Sent to AI: {current_state}")

        # 2. Query our newly created AI brain instead of an input box
        ai_chosen_move = query_llm_for_action(current_state)
        print(f"[ACTION EXECUTED]: {ai_chosen_move}")

        # 3. Apply the move to the board grid
        game_over = world.step(ai_chosen_move)

    if game_over:
        print(f"\n🎉 Success! Target was reached in {world.moves_taken} moves.")
    else:
        print("\n❌ Mission failed: The AI loop timed out or got stuck.")


if __name__ == "__main__":
    main()