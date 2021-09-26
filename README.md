# SimpleMaze

## Quick Start

```
from SimpleMaze_JJAP import maze
import os
now = os.getcwd()


a = maze()
a.create(200 , 200)
a.save(False , 10 , now + "\\200x200 maze.jpg")  # No answer
a.save(True , 10 , now + "\\200x200 maze_answer.jpg") # With answer
```

## Functions

### **1. self.create(x,y)**

create maze and save that maze.

self.maze : data of maze (list)

self.image : data of maze(no answer) image

self.answerImage : data of maze(answer) image

### **2. self.save(answer,size,location)**

make image file with self.image and self.answerImage. 

answer : True or False. True, the image have answer

size : the size of one block(px). I recommend 10.

location : the location of file. It is **not relative**.



made by JJAPDABOTTEAM

1. Seol7523
2. Mossygoldcoin

