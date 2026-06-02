class GridWorld:
    def __init__(self):
        #defining a 5x5 grid
        self.agent_pos=[0,0]    #bot starts in top left
        self.target_pos=[3,3]   #target is in the middle of the grid
        self.moves_taken=0


    def get_observation_text(self):
        """translating grid state in to text state for AI"""
        return(
            f"You are a robot in a 5x5 grid world. "
            f"Your current position is {self.agent_pos}."
            f"The target objective is located at {self.target_pos}."
            f"Available moves: [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]."
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
    

    def main():
        """main control loop for our application"""
        world=GridWorld()
        game_over=False

        print("Game started! Type a move to play")

        while not game_over:
            #show the world in text
            print("\n"+world.get_observation_text())

            #get input from user in the terminal
            user_move=input("Enter action: ").strip().upper()

            #run the move
            game_over = world.step(user_move)


        print("Success! Target was reached in {world.moves_taken} moves.")