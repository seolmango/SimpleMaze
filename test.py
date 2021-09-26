from SimpleMaze_JJAP import maze
import os
now = os.getcwd()


a = maze.Maze()
a.create(200 , 200)
a.save(False , 10 , now + "\\200x200 maze.jpg")  # No answer
a.save(True , 10 , now + "\\200x200 maze_answer.jpg") # With answer