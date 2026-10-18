
from PIL import Image
import datetime
import random
import pygame
import cv2
import sys
import os

def convert(image):
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()

state_previous = ""
state = "video"
state_context_previous = ""
state_context = "idle"
state_counter = 0
state_time = 0.0
window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
run = True
video = None
image = None
then = datetime.datetime.now()

while (run):
    if (sys.flags.debug):
        print(str(state_counter))
    now = datetime.datetime.now()
    delta = now-then
    delta = float(delta.total_seconds())
    then = now
    if not (state == state_previous):
        if (state == "video"):
            success = True
            try:
                video = cv2.VideoCapture(state_context+".mp4")
            except:
                success = False
            if not (success):
                video = None
            if not (video is None):
                fps = video.get(cv2.CAP_PROP_FPS)
        else:
            if (state == "image"):
                try:
                    image = Image.open(state_context+".png")
                    image = convert(image)
                except:
                    image = None
            if (state_previous == "video"):
                fps = None
        state_context_previous = state_context
        state_previous = state
        state_counter = 0
        state_time = 0.0
    else:
        if (state == "video"):
            if not (state_context == state_context_previous):
                success = True
                try:
                    video = cv2.VideoCapture(state_context+".mp4")
                except:
                    success = False
                if not (success):
                    video = None
                if not (video is None):
                    fps = video.get(cv2.CAP_PROP_FPS)
                state_context_previous = state_context
                state_previous = state
                state_counter = 0
                state_time = 0.0
            if (state_context == "idle"):
                if ((state_time > 120.0) or ((state_time > 5.0) and (state_counter%random.randint(2, 10000) == random.randint(0, 2000)))):
                    print(str(state_time))
                    print(str(state_counter))
                    if (random.randint(0, 100) < 50):
                        state_context = "knuckle_crack"
                    else:
                        state_context = "knuckle_crack_other"
        state_counter += 1
        state_time += delta
    if not (fps is None):
        clock.tick(fps)
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
    if not (run):
        continue
    if (state == "video"):
        if not (video is None):
            success, video_image = video.read()
            surface = None
            if (success):
                surface = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                if ((state_context == "knuckle_crack") or (state_context == "knuckle_crack_other")):
                    state_context = "idle"
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
    pygame.display.flip()

pygame.quit()
exit()

