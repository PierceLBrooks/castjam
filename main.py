
from PIL import Image
import datetime
import pygame.freetype
import pygame
import random
import json
import cv2
import sys
import os

def convert(image):
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()

if not (__name__ == "__main__"):
    sys.exit()

pygame.init()
next = -1
stage_previous = -1
stage = 0
state_previous = ""
state = "video"
context_previous = ""
context = "idle"
state_counter = 0
state_time = 0.0
width = 1280.0
height = 720.0
window = pygame.display.set_mode((int(width), int(height)))
font = pygame.freetype.Font(os.path.join(os.getcwd(), "antarctica.ttf"), 24)
clock = pygame.time.Clock()
run = True
video = None
image = None
then = datetime.datetime.now()
color = [255, 255, 255]
text = []
charge = 0.0
typing = 0.0
mouse = 0.0
life = 0.0
transition = 0.0
fps = None
descriptor = open(os.path.join(os.getcwd(), os.path.basename(sys.argv[0])+".json"), "r")
data = descriptor.read()
descriptor.close()
stages = json.loads(data)
if ((stage >= 0) and (stage < len(stages))):
    if ("trigger" in stages[stage]):
        trigger = stages[stage]["trigger"]
    if (("state" in stages[stage]) and (len((stages[stage]["state"])) > 0)):
        state = stages[stage]["state"]
    if (("context" in stages[stage]) and (len((stages[stage]["context"])) > 0)):
        context = stages[stage]["context"]
    if ("text" in stages[stage]):
        text = stages[stage]["text"]
    if ("next" in stages[stage]):
        next = stages[stage]["next"]
    if ("mouse" in stages[stage]):
        mouse = stages[stage]["mouse"]
    if ("typing" in stages[stage]):
        typing = stages[stage]["typing"]

while (run):
    """
    if (sys.flags.debug):
        print(str(state_counter))
        print(str(stages[stage]))
    """
    now = datetime.datetime.now()
    delta = now-then
    delta = float(delta.total_seconds())
    then = now
    life += delta
    transition += delta
    if (stage == stage_previous):
        if ((trigger == "timing") and (transition > stages[stage]["timing"])):
            stage = next
            transition = 0.0
        elif ((trigger == "charge") and (charge > stages[stage]["charge"])):
            stage = next
            transition = 0.0
    if (typing > 0.0):
        if ((stage == stage_previous) and (trigger == "typing")):
            stage = next
            transition = 0.0
        if not (mouse > 0.0):
            charge += delta
        typing -= delta
        if (typing <= 0.0):
            typing = 0.0
            if not (mouse > 0.0):
                if ((state == "video") and ("typing" in context)):
                    context = "idle"
            else:
                if ((state == "video") and ("click" in context)):
                    context = "mouse_move"
    else:
        if not (mouse > 0.0):
            charge -= delta
        else:
            charge -= delta*2.5
        if (charge < 0.0):
            charge = 0.0
    if (mouse > 0.0):
        if ((state == "video") and (context == "mouse_move")):
            mouse -= delta
            if (mouse <= 0.0):
                context = "from_mouse"
    if not (stage == stage_previous):
        transition = 0.0
        mouse = 0.0
        typing = 0.0
        if ((stage >= 0) and (stage < len(stages))):
            if ("trigger" in stages[stage]):
                trigger = stages[stage]["trigger"]
            if (("state" in stages[stage]) and (len((stages[stage]["state"])) > 0)):
                state = stages[stage]["state"]
            if (("context" in stages[stage]) and (len((stages[stage]["context"])) > 0)):
                context = stages[stage]["context"]
            if ("text" in stages[stage]):
                text = stages[stage]["text"]
            if ("next" in stages[stage]):
                next = stages[stage]["next"]
            if ("mouse" in stages[stage]):
                mouse = stages[stage]["mouse"]
            if ("typing" in stages[stage]):
                typing = stages[stage]["typing"]
        stage_previous = stage
    if not (state == state_previous):
        if (state == "video"):
            success = True
            try:
                video = cv2.VideoCapture(os.path.join(os.getcwd(), context+".mp4"))
            except:
                success = False
            if not (success):
                video = None
            if not (video is None):
                fps = video.get(cv2.CAP_PROP_FPS)
        else:
            if (state == "image"):
                try:
                    image = Image.open(os.path.join(os.getcwd(), context+".png"))
                    image = convert(image)
                except:
                    image = None
            if (state_previous == "video"):
                fps = None
        context_previous = context
        state_previous = state
        state_counter = 0
        state_time = 0.0
    else:
        if (state == "video"):
            if not (context == context_previous):
                success = True
                try:
                    video = cv2.VideoCapture(os.path.join(os.getcwd(), context+".mp4"))
                except:
                    success = False
                if not (success):
                    video = None
                if not (video is None):
                    fps = video.get(cv2.CAP_PROP_FPS)
                context_previous = context
                state_previous = state
                state_counter = 0
                state_time = 0.0
            if (context == "idle"):
                if ((state_time > 90.0) or ((state_time > 5.0) and (state_counter%random.randint(2, 10000) == random.randint(0, 2000)))):
                    if (sys.flags.debug):
                        print(str(state_time))
                        print(str(state_counter))
                    if (random.randint(0, 100) < 50):
                        context = "knuckle_crack"
                    else:
                        context = "knuckle_crack_other"
        else:
            if (state == "image"):
                try:
                    image = Image.open(os.path.join(os.getcwd(), context+".png"))
                    image = convert(image)
                except:
                    image = None
        state_counter += 1
        state_time += delta
    if not (fps is None):
        clock.tick(fps)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
        elif event.type == pygame.KEYDOWN:
            if not (mouse > 0.0):
                if (typing < 1.0):
                    typing = 1.0
                if ((state == "video") and (context == "idle")):
                    context = "long_typing"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (typing < 1.0):
                typing = 1.0
            if not (mouse > 0.0):
                if not (context == "from_mouse"):
                    context = "to_mouse"
            else:
                if (context == "mouse_move"):
                    context = "mouse_click"
                    charge += 5.0
            if (mouse < 2.5):
                mouse = 2.5
    if not (run):
        continue
    if (state == "video"):
        if not (video is None):
            success, video_image = video.read()
            surface = None
            if (success):
                surface = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                if ((context == "knuckle_crack") or (context == "knuckle_crack_other") or (context == "from_monitor") or (context == "from_mouse")):
                    mouse = 0.0
                    typing = 0.0
                    context = "idle"
                elif (context == "to_monitor"):
                    state = "image"
                    context = "from_monitor"
                elif ((context == "to_mouse") or (context == "mouse_click")):
                    context = "mouse_move"
                else:
                    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    success, video_image = video.read()
                    if (success):
                        surface = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            if not (surface is None):
                window.blit(surface, (0, 0))
    elif (state == "image"):
        if not (image is None):
            window.blit(image, (0, 0))
    elif (state == "color"):
        try:
            window.fill(tuple(context))
        except:
            pass
    if (len(text) > 0):
        offset = 0.0
        size = [width, 0.0]
        blit = [0.0, height]
        for i in range(len(text)):
            render, bounds = font.render(text[i], tuple(color))
            """
            if (sys.flags.debug):
                print(str(bounds))
                print(str(bounds.width))
                print(str(bounds.height))
            """
            if (i == 0):
                offset += float(bounds.height)*1.5
            blit[1] -= float(bounds.height)*1.5
        """
        if (sys.flags.debug):
            print(str(size))
            print(str(blit))
        """
        size[0] = int(size[0])
        size[1] = int(blit[1]*2.0)
        blit[0] = int(blit[0])
        blit[1] = int(blit[1]-(height-blit[1]))
        rectangle = pygame.Surface(tuple(size))
        rectangle.set_alpha(128)
        rectangle.fill((0, 0, 0))
        window.blit(rectangle, tuple(blit))
        for i in range(len(text)):
            render, bounds = font.render(text[i], tuple(color))
            position = []
            position.append(width*0.5)
            position.append(blit[1]+(offset*float(i+1)))
            position[0] -= float(bounds.width*0.5)
            position[0] -= float(bounds.height*0.5)
            position[0] = int(position[0])
            position[1] = int(position[1])
            window.blit(render, tuple(position))
    pygame.draw.rect(window, (255, 255, 255), (14, 14, 164, 36))
    pygame.draw.rect(window, (0, 0, 0), (16, 16, 160, 32))
    pygame.draw.rect(window, (int(255.0*(1.0-min(1.0, charge/100.0))), int(255.0*min(1.0, charge/100.0)), 0), (18, 18, int(160.0*(charge/100.0)), 28))
    pygame.display.flip()

pygame.quit()
exit()

