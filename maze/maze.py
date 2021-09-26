import random
from PIL import Image


# [미로 픽셀] 0: 확인되지 않음, 1: 길, 2: 정답 길, 3: 벽, 4: 입구, 5: 출구
mazeColor = {0: (127, 127, 127), 1: (255, 255, 255), 2: (255, 127, 0), 3: (0, 0, 0), 4: (0, 255, 0), 5: (255, 0, 0)}


class maze():


    def create(self, width : int, height : int):
        """
        가로가 width칸이고 세로가 height칸인 미로를 제작합니다
        아직 사진으로 저장된 것은 아닙니다
        """

        self.width = width
        self.height = height
        self.maze = []
        answerLoad = []
        for i in range(height * 2 + 1):
            self.maze.append([])
            answerLoad.append([])
            for j in range(width * 2 + 1):
                if i % 2 == 0 or j % 2 == 0:
                    self.maze[i].append(3)
                else:
                    self.maze[i].append(0)
                answerLoad[i].append(0)
        self.maze[1][0] = 4
        self.maze[height * 2 - 1][width * 2] = 5
        
        notBlockedLoad = []

        # creater가 길 하나를 뚫는 함수
        def createLoad(createrY, createrX):

            notBlockedMove = []
            
            first = True
            while first or len(notBlockedMove):
                
                if first:
                    first = False
                else:
                    # 길 한칸을 뚫기, first로 처음에 못 뚫게한 이유는 처음에는 아무정보가 없기때문.
                    move = random.choice(notBlockedMove)
                    self.maze[createrY + move[0]][createrX + move[1]] = 1
                    createrX += move[1] * 2
                    createrY += move[0] * 2
                    del notBlockedLoad[notBlockedLoad.index([createrY, createrX])]
                    self.maze[createrY][createrX] = 1
                    answerLoad[createrY][createrX] = move[0] + move[1] * 2 # [-1,0] = -1, [1,0] = 1, [0,-1] = -2, [0,1] = 2

                # creater 주변에 막히지 않은 길 구하기, notBlocked'Move' 라 이름을 지은이유는 나중에 저거대로 움직여야하기 때문.
                notBlockedMove = []
                if 1 < createrX:
                    if self.maze[createrY][createrX - 2] == 0:
                        notBlockedMove.append([0, -1])
                        if not [createrY, createrX - 2] in notBlockedLoad:
                            notBlockedLoad.append([createrY, createrX - 2])
                if createrX < width * 2 - 1:
                    if self.maze[createrY][createrX + 2] == 0:
                        notBlockedMove.append([0, 1])
                        if not [createrY, createrX + 2] in notBlockedLoad:
                            notBlockedLoad.append([createrY, createrX + 2])
                if 1 < createrY:
                    if self.maze[createrY - 2][createrX] == 0:
                        notBlockedMove.append([-1, 0])
                        if not [createrY - 2, createrX] in notBlockedLoad:
                            notBlockedLoad.append([createrY - 2, createrX])
                if createrY < height * 2 - 1:
                    if self.maze[createrY + 2][createrX] == 0:
                        notBlockedMove.append([1, 0])
                        if not [createrY + 2, createrX] in notBlockedLoad:
                            notBlockedLoad.append([createrY + 2, createrX])

        # creater가 모든길을 뚫게 하기
        createrX, createrY = 1, 1
        self.maze[1][1] = 1
        createLoad(1, 1)
        
        while len(notBlockedLoad):
            
            [createrY, createrX] = random.choice(notBlockedLoad)
            del notBlockedLoad[notBlockedLoad.index([createrY, createrX])]
            self.maze[createrY][createrX] = 1
            blockedMove = []
            if 1 < createrX:
                if self.maze[createrY][createrX - 2] != 0:
                    blockedMove.append([0, -1])
            if createrX < width * 2 - 1:
                if self.maze[createrY][createrX + 2] != 0:
                    blockedMove.append([0, 1])
            if 1 < createrY:
                if self.maze[createrY - 2][createrX] != 0:
                    blockedMove.append([-1, 0])
            if createrY < height * 2 - 1:
                if self.maze[createrY + 2][createrX] != 0:
                    blockedMove.append([1, 0])
            move = random.choice(blockedMove)
            self.maze[createrY + move[0]][createrX + move[1]] = 1
            answerLoad[createrY][createrX] = -(move[0] + move[1] * 2) # [1,0] = -1, [-1,0] = 1, [0,1] = -2, [0,-1] = 2
            createLoad(createrY, createrX)

        # 정답 리스트에 표시하기
        createrX, createrY = width * 2 - 1, height * 2 - 1
        self.maze[createrY][createrX] = 2
        while createrX != 1 or createrY != 1:
            if answerLoad[createrY][createrX] == 1:
                createrY -= 1
                self.maze[createrY][createrX] = 2
                createrY -= 1
                self.maze[createrY][createrX] = 2
            elif answerLoad[createrY][createrX] == -2:
                createrX += 1
                self.maze[createrY][createrX] = 2
                createrX += 1
                self.maze[createrY][createrX] = 2
            elif answerLoad[createrY][createrX] == -1:
                createrY += 1
                self.maze[createrY][createrX] = 2
                createrY += 1
                self.maze[createrY][createrX] = 2
            elif answerLoad[createrY][createrX] == 2:
                createrX -= 1
                self.maze[createrY][createrX] = 2
                createrX -= 1
                self.maze[createrY][createrX] = 2
            
        # 사진 만들기
        self.image = Image.new("RGB", (self.width * 2 + 1, self.height * 2 + 1), (0, 0, 0))
        imagePixel = self.image.load()
        for i in range(width * 2 + 1):
            for j in range(height * 2 + 1):
                if self.maze[j][i] == 2:
                    imagePixel[i, j] = (255, 255, 255)
                else:
                    imagePixel[i, j] = mazeColor[self.maze[j][i]]
                    
        # 정답사진 만들기
        self.answerImage = Image.new("RGB", (self.width * 2 + 1, self.height * 2 + 1), (0, 0, 0))
        answerImagePixel = self.answerImage.load()
        for i in range(width * 2 + 1):
            for j in range(height * 2 + 1):
                answerImagePixel[i, j] = mazeColor[self.maze[j][i]]


    def save(self, answer, size , location):
        """
        미로의 사진을 location에 저장합니다.answer는 정답을 표시할지 여부이고 size만큼 키워서 저장합니다
        """

        if answer:
            self.answerImage = self.answerImage.resize(((self.width * 2 + 1) * size, (self.height * 2 + 1) * size), resample = False)
            self.answerImage.save(location)
        else:
            self.image = self.image.resize(((self.width * 2 + 1) * size, (self.height * 2 + 1) * size), resample = False)
            self.image.save(location)


if __name__ == '__main__':
    import os
    now = os.getcwd()
    print('미로 제작중')
    a = maze()
    a.create(200 , 200)
    a.save(False , 10 , now + "\\200x200 maze.jpg")
    a.save(True , 10 , now + "\\200x200 maze_answer.jpg")
