import pyxel, math, random


temp_framecount = 0


class Object: 


    def __init__(self, state):
        self.speed = 3
        self.state = state
        self.restart()


    def update(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        if self.x >= 190:
            self.vx = -self.vx
        elif self.x <= 0:
            self.vx = -self.vx
        
        if self.y >= 170:
            self.restart()
            return True


    def restart(self):
        self.x = random.randint(0, 170)
        self.y = 0
        
        if self.state:
            angle = math.radians(90)
        else:
            angle = math.radians(random.randint(30,150))
        
        self.vx = math.cos(angle)
        self.vy = math.sin(angle)


    def draw(self):
        if self.state:
            pyxel.blt(self.x, self.y, 0, 7, 99, 18, 29, 10) 
        else: 
            pyxel.blt(self.x, self.y, 0, 9, 58, 14, 31, 10)



class Shark:


    def __init__(self):
        self.y = 148
        self.w = 30
        self.h = 58


    def update(self):
        self.x = pyxel.mouse_x


    def capture(self, object):
        if object.x >= self.x-2 and object.x <= self.x+self.w and object.y >=160:
            object.restart()
            return True
    

    def draw(self):  
        pyxel.blt(self.x, self.y, 2, 5, 6, self.w, self.h, 10) 



class textanime:


    def write_text(y, text, color, width=200, spacing=10):
        margin = width // 20

        def centerTextX(txt):
            return width / 2 - len(txt) / 2 * 4 + margin / 2

        max_length = width - 2 * margin
        split_text = text.split() 
        line_count = 1 
        char_count = 0
        lines = [[]]
        for word in split_text:
            if char_count > max_length:
                lines[line_count - 1].pop(-1)
                lines.append([])
                line_count += 1
                char_count = len(word)

            char_count += 4 * (len(word) + 1)
            lines[line_count - 1].append(word)
            if word[-1] == "." or word[-1] == "?" or word[-1] == "!" or word == ":(" or word == ":)":
                line_count += 1
                char_count = 0
                lines.append([])

        for i, line in enumerate(lines):
            new_line = " "
            for word in line:
                new_line += word + " "
            lines[i] = new_line
        for i, line in enumerate(lines):
            x = centerTextX(line)
            pyxel.text(x, y + i * spacing, line, color)
        

    def write_text_slowly(y, text, color, width, starting_time, character_speed=1, spacing=8):
        global temp_framecount
        if starting_time is None:
            starting_time = temp_framecount
        textanime.write_text(y, text[0: int((temp_framecount - starting_time) / character_speed)], color, width, spacing)



class Bounce:


    def __init__(self, x, y, pic):
        self.x = x
        self.y = y
        self.pic = pic
        self.w = 15
        self.h = 15

        self.vy = math.sin(90)
        self.speed = 0.5


    def update(self):
        if self.pic == 1:
            if self.y < 70 or self.y + self.h > 100:
                self.vy *= -1

        elif self.pic == 2:
            if self.y < 35 or self.y + self.h > 100:
                self.vy *= -1

        elif self.pic == 3:
            if self.y < 120 or self.y + self.h > 150:
                self.vy *= -1

        self.y += self.vy * self.speed


    def draw(self):
        if self.pic == 1:
            pyxel.blt(self.x, self.y, 0, 6, 7, 20, 44, 10)
        elif self.pic == 2:
            pyxel.blt(self.x, self.y, 0, 7, 99, 18, 29, 10)
        elif self.pic == 3:
            pyxel.blt(self.x, self.y, 0, 9, 58, 14, 31, 10)



class NameBounce:


    def __init__(self, x, y, pic):
        self.x = x
        self.y = y
        self.pic = pic
        self.w = 15
        self.h = 15
        self.vx = math.cos(90)
        self.speed = 0.5


    def update(self):
        if self.pic == 1:
            if self.x < 60 or self.x + self.w > 85:
                self.vx *= -1

        elif self.pic == 2:
            if self.x < 40 or self.x + self.w > 70:
                self.vx *= -1

        self.x += self.vx * self.speed


    def draw(self):
        if self.pic == 1:
            pyxel.blt(self.x, self.y,0,3,173,78,24,7)
        elif self.pic == 2:
            pyxel.blt(self.x, self.y,0,4,205,106,24,7)



class WelcomePage:


    def __init__(self, visible):
        self.visible = visible
        self.bounce = [Bounce(25,85,1),Bounce(160,50,2),Bounce(170,120,3)]
        self.namebounce = [NameBounce(65,90,1),NameBounce(50,130,2)]


    def update(self):
        for bounce in self.bounce:
            bounce.update()
        
        for name in self.namebounce:
            name.update()
    

    def draw(self): 
        pyxel.rect(96,29,16,7,12)
        pyxel.rect(84,59,41,7,12)
        pyxel.text(97,30, "HEY!", pyxel.frame_count % 16)
        pyxel.text(85,60, "WELCOME TO", pyxel.frame_count % 16)
        
        for bounce in self.bounce:
            bounce.draw()
            
        for name in self.namebounce:
            name.draw()
            
        pyxel.rect(55,174,95,7,12)
        textanime.write_text_slowly(175, "Press SPACE to continue", 1, 200, 0, character_speed=1, spacing=50)



class MenuPage:


    def __init__(self, r, visible):
        self.runmore = r
        self.visible = visible


    def update(self):
        pass


    def draw(self):
        pyxel.rect(48,19,109,7,12)
        if not self.runmore:
            pyxel.rect(86,49,34,7,12)
            pyxel.rect(83,79,39,7,12)
            pyxel.rect(80,109,47,7,12)
            pyxel.rect(86,139,35,7,12)
            pyxel.rect(18,179,170,7,12)
            textanime.write_text_slowly(20, "What would you like to do? 1) PLAY. 2) RULES. 3) CONTEXT. 4) EXIT.", 2, 200, 0, character_speed=2, spacing=30)
            textanime.write_text_slowly(180, "Press key corresponding to option number!!", 15, 200, 0, character_speed=2, spacing=40)
        else:
            pyxel.rect(86,59,34,7,12)
            pyxel.rect(83,99,39,7,12)
            pyxel.rect(80,139,47,7,12)
            pyxel.rect(86,179,35,7,12)
            textanime.write_text(20, "What would you like to do? 1) PLAY. 2) RULES. 3) CONTEXT. 4) EXIT.", 2, spacing=40)



class RulesPage:


    def __init__(self, r, visible):
        self.runmore = r
        self.visible = visible


    def update(self):
        pass


    def draw(self):
        pyxel.cls(12)
        
        if not self.runmore: #runmore = when user pressed 2) rules more than once
            textanime.write_text_slowly(10, "Don't let DaBaby get away! If you catch Dababy, 2 POINTS +1 HEALTH :) If you catch a pet bottle, health = -10 :( If you lose > 15 babies, GAME OVER. If you health = 0, GAME OVER. If SCORE = 100, YOU WIN!", 1, 200, 0, character_speed=2, spacing=30)
        else:
            textanime.write_text(10, "Don't let DaBaby get away! If you catch Dababy, 2 POINTS +1 HEALTH :) If you catch a pet bottle, health = -10 :( If you lose > 15 babies, GAME OVER. If health = 0, GAME OVER. If SCORE = 100, YOU WIN!", 1, spacing=30)
        textanime.write_text_slowly(180, "Press SPACE to go back to menu", pyxel.frame_count%16, 200, 0, character_speed=0.5, spacing=50)
 


class ContextPage:


    def __init__(self, r, visible):
        self.runmore = r
        self.visible = visible


    def update(self):
        pass


    def draw(self):
        pyxel.cls(12)
        if not self.runmore: #runmore = when user pressed 3) context more than once
            textanime.write_text_slowly(40, "Dababy is a bad boy. Dababy keeps littering the ocean with plastic. Help the shark get rid of Dababy. Avoid pet bottles while at it!", 1, 200, 0, character_speed=2, spacing=30)
        else:
            textanime.write_text(40, "Dababy is a bad boy. Dababy keeps littering the ocean with plastic. Help the shark get rid of Dababy. Avoid pet bottles while at it! ", 1, spacing=30)
        textanime.write_text_slowly(180, "Press SPACE to go back to menu", pyxel.frame_count%16, 200, 0, character_speed=0.5, spacing=50)



class Game:


    def __init__(self, highscore=0):
        self.objects = [Object(True), Object(False), Object(False)] #Baby, bottle, bottle
        self.shark = Shark()
        self.eaten = False
        self.score = 0 
        self.loss = 0 
        self.ruleshow = False
        self.winscore = False
        self.health = 100
        self.condition = False
        self.progress = True
        self.visible = False
        self.highscore = highscore
    

    def update(self):
        if self.progress and self.visible: 
            self.ruleshow = True
            speed_change = False
            self.shark.update()

            for object in self.objects:
                result = object.update()
                capture = self.shark.capture(object)
                
                if result and object.state: #if restarted and it was a baby
                    self.condition = False
                    self.eaten = False
                    self.loss += 1     #you miss babies
                    
                    if self.loss >= 15:
                        pyxel.playm(1)
                        self.ruleshow = False
                        self.progress = False
                        break 
                
                elif result and not object.state:
                    self.eaten = False

                elif capture and object.state:
                    pyxel.playm(3)
                    self.condition = False
                    self.eaten = True
                    
                    if self.health < 100:
                        self.health += 1
                    self.score += 2
                    speed_change = True
                    
                    if self.score % 20 == 0:
                        self.objects.append(Object(True))
                    elif self.score % 50 == 0:
                        self.objects.append(Object(False))
                    
                    if self.score == 100:
                        pyxel.playm(4, loop=-1) 
                        self.ruleshow = False
                        self.winscore = True
                        self.progress = False
                        break
                
                elif capture and not object.state:
                    pyxel.playm(2)
                    self.eaten = False
                    object.x = random.randint(0,170)
                    object.y = 0 
                    self.health -= 10
                    
                    if self.health <= 30:
                        self.condition = True
                    if self.health <= 0:
                        pyxel.playm(1) 
                        self.ruleshow = False
                        self.condition = False
                        self.progress = False
                        break 

                if speed_change:
                    object.speed += 0.05


    def draw(self):
        if self.visible:
            for object in self.objects:
                object.draw()

            if self.condition:
                pyxel.rect(75, 59, 55, 7, 12)
                textanime.write_text(60, "CONDITION POOR", pyxel.frame_count%16, spacing=30)

            if self.eaten: #68 70
                pyxel.blt(self.shark.x, self.shark.y, 2, 45, 6 , 27, 64, 10) 
            else:
                self.shark.draw()
            
            if not self.progress:
                pyxel.rect(48,79,108,7,12)
                pyxel.rect(74,99,56,7,12)
                pyxel.rect(83,119,37,7,12)
                pyxel.rect(80,139,45,7,12)
                pyxel.rect(86,159,32,7,12)
                textanime.write_text(80, "What would you like to do? 1) PLAY AGAIN. 2) RULES. 3) CONTEXT. 4) EXIT.", 2, spacing=20)

                if self.winscore:
                    for i in range (0,pyxel.frame_count, 50):  
                        if pyxel.frame_count > i and pyxel.frame_count <= i+20:
                            pyxel.blt(150,140,2,3,68,29,29,7) #32,97  #first
                            pyxel.blt(17,97,2,48,65,36,36,7) #84,101 #second
                        elif pyxel.frame_count > i+20 and pyxel.frame_count <= i+50:
                            pyxel.blt(20,100,2,3,68,29,29,7) #32,97    #first 
                            pyxel.blt(147,137,2,48,65,42,36,7) #84,101 #second

                    pyxel.rect(75, 59, 55, 7, 12)
                    textanime.write_text_slowly(60, "YOU WON !!", pyxel.frame_count%16, 200, 0, character_speed=0.05, spacing=50)

                else:
                    pyxel.rect(75, 59, 55, 7, 12)
                    textanime.write_text_slowly(60, "YOU LOST :(", pyxel.frame_count%16, 200, 0, character_speed=0.05, spacing=50)

            if self.ruleshow:
                pyxel.rect(9, 49, 100, 7, 12)
                pyxel.text(10,50,"Use MOUSE to move shark!!", pyxel.frame_count%16)

            pyxel.rect(0,0,115,47,0)
            pyxel.rect(0,0,114,46,12)
            pyxel.text(5, 5, f"Score: {self.score}",2)
            pyxel.text(5, 15, f"Missed babies ( <15 ) : {self.loss}",2) 
            
            if self.health<0:
                pyxel.text(5, 25, f"Health : {0}",2) 
            else:
                pyxel.text(5, 25, f"Health : {self.health}",2) 
            
            if self.highscore > 0:
                curr_highscore = self.highscore
            else:
                curr_highscore = "N/A"

            pyxel.text(5, 35, f"Highest score: {curr_highscore}",2)



class App:


    def __init__(self):
        pyxel.init(200,200, caption = "Baby Shark")
        pyxel.load("shark.pyxres")
        pyxel.mouse(True)
        self.pages = [WelcomePage(True), MenuPage(False, False), RulesPage(False, False), ContextPage(False,False)]
        self.highest = []
        self.visible = True
        self.game = Game()
        self.runmore = 0
        self.exit = False
        pyxel.playm(0, loop =-1)
        pyxel.run(self.update, self.draw)
    

    def update(self):
        global temp_framecount
        temp_framecount += 1

        if self.pages[0].visible:

            if pyxel.btnp(pyxel.KEY_SPACE):
                temp_framecount = 0
                self.pages[0].visible = False
                self.pages[1].visible = True
        
        elif self.pages[1].visible:

            if pyxel.btnp(pyxel.KEY_1):
                temp_framecount = 0
                pyxel.playm(5)
                self.game.visible = True
                self.pages[1].visible = False
                
            elif pyxel.btnp(pyxel.KEY_2):
                temp_framecount = 0
                self.pages[1].visible = False
                self.pages[2].visible = True

                self.pages[1].runmore = True
            
            elif pyxel.btnp(pyxel.KEY_3):
                temp_framecount = 0
                self.pages[1].visible = False
                self.pages[3].visible = True

                self.pages[1].runmore = True

            elif pyxel.btnp(pyxel.KEY_4):
                pyxel.playm(6)
                temp_framecount = 0
                self.pages[1].visible = False
                self.exit = True
        
        elif self.pages[2].visible:

            if pyxel.btnp(pyxel.KEY_SPACE):
                temp_framecount = 0
                self.pages[2].visible = False
                self.pages[1].visible = True

                self.pages[2].runmore = True

        elif self.pages[3].visible:

            if pyxel.btnp(pyxel.KEY_SPACE):
                temp_framecount = 0
                self.pages[3].visible = False
                self.pages[1].visible = True

                self.pages[3].runmore = True

        elif self.game.visible and not self.game.progress: #if game is visible but is over
            if pyxel.btnp(pyxel.KEY_1): #for retrying 
                pyxel.playm(5)
                self.highest.append(self.game.score)
                self.game = Game(highscore = max(self.highest))
                self.game.visible = True

            elif pyxel.btnp(pyxel.KEY_2):
                temp_framecount = 0
                self.pages[1].visible = False
                self.pages[2].visible = True
                self.pages[1].runmore = True
                self.highest.append(self.game.score)
                self.game = Game(highscore = max(self.highest))

            elif pyxel.btnp(pyxel.KEY_3):
                temp_framecount = 0
                self.pages[1].visible = False
                self.pages[3].visible = True
                self.pages[1].runmore = True
                self.highest.append(self.game.score)
                self.game = Game(highscore = max(self.highest))

            elif pyxel.btnp(pyxel.KEY_4):
                pyxel.playm(6)
                temp_framecount = 0
                self.pages[1].visible = False
                self.game.visible = False
                self.exit = True

        for page in self.pages:
            if page.visible:
                page.update()
        
        self.game.update()
    

    def draw(self):
        pyxel.bltm(0,0,0,0,0,100,120)

        if self.exit:
            pyxel.cls(12)
            textanime.write_text_slowly(100,"Sad to see you leave :(", 1, 200, 0, character_speed=2, spacing=50)
            if temp_framecount == 130:
                pyxel.quit()

        else:
            for page in self.pages:
                if page.visible:
                    page.draw()

        self.game.draw()
      
App()