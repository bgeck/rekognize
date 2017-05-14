"""
Interactive art experiment that examines social issues around AI and machine learning.

This project takes a look at some of the new issues arising in machine learning and AI tech,
including problems such as accidental racism and sexism caused by arbitrary machine decisions.
By using the Rekognize API, which detects not only expression in faces,
but also gender, race, age, and even a "beauty" score, I examine how arbitrary decisions programmed
into systems could very easily fall down a slippery slope and cause groups to be
discriminated against.
"""
import json
import sys
import time
from base64 import b64encode

import pygame
import requests
from SimpleCV import Camera, Display

from pillow import (Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont,
                    ImageOps)

# when running this project, pass in the key and secret via command line.
# Little more secure.
REKOGNITION_KEY = sys.argv[0]
REKOGNITION_SECRET = sys.argv[1]
URL = "http://rekognition.com/func/api/"
WEBCAM = Camera()
VIDEO_DISPLAY = Display()


def play_video(image_file):
    """
    Get video feed from camera and save frame on mouse click.

    :param image_file: - The image file location to save to.
    :type image_file: str
    """
    while VIDEO_DISPLAY.isNotDone():
        webcam_image = WEBCAM.getImage().scale(800, 450).show()

        if VIDEO_DISPLAY.mouseLeft:
            webcam_image.save(image_file)
            break
    return


def transform_image(image_file, data):
    """
    Make 'decisions' about image based on sex, race, age, and beauty.

    :param image_file: - The image file to transform.
    :type image_file: str
    :param data: - The data returned from Rekognize.
    :type data: dict
    """
    static_image = Image.open(image_file)

    if data['found_race'] != "white":
        enhanced_color = ImageEnhance.Color(static_image)
        step1 = enhanced_color.enhance(0)
    else:
        step1 = static_image

    if data['decided_sex'] != 1:
        step2 = ImageOps.equalize(step1, None)
    else:
        step2 = step1

    step3 = step2.filter(ImageFilter.GaussianBlur(
        1 / (data['found_beauty'] * 2)))

    if data['found_age'] > 35:
        step4 = ImageOps.autocontrast(step3, 20, None)
    else:
        step4 = step3
    return step4


def display_image(image_file, data):
    """
    Display transformed image.

    :param image_file: - The image file to dispaly.
    :type image_file: str
    :param data: - The data returned from Rekognize.
    :type data: dict
    """
    static_image = Image.open(image_file)
    current_text = Image.new('RGBA', static_image.size, (255, 255, 255, 0))
    current_rect = Image.new('RGBA', static_image.size, (255, 255, 255, 0))
    current_font = ImageFont.truetype('AppleGothic.ttf', 26)

    xvalue1 = 0
    yvalue1 = 5
    xvalue2 = 240
    yvalue2 = 42

    current_box = ImageDraw.Draw(current_rect)
    current_box.rectangle(
        [xvalue1, yvalue1, xvalue2, yvalue2],
        fill=(0, 0, 0, 255),
        outline=None)
    current_box.rectangle(
        [xvalue1, yvalue1 + 42, xvalue2, yvalue2 + 47],
        fill=(0, 0, 0, 255),
        outline=None)
    current_box.rectangle(
        [xvalue1, yvalue1 + 89, xvalue2, yvalue2 + 92],
        fill=(0, 0, 0, 255),
        outline=None)
    current_box.rectangle(
        [xvalue1, yvalue1 + 134, xvalue2, yvalue2 + 137],
        fill=(0, 0, 0, 255),
        outline=None)

    current_drawing = ImageDraw.Draw(current_text)
    current_drawing.text(
        (10, 10), "Sex: " + data['decided_sex'],
        font=current_font,
        fill=(255, 255, 255, 255))
    current_drawing.text(
        (10, 55), "Age: " + str(int(data['found_age'])),
        font=current_font,
        fill=(255, 255, 255, 255))
    current_drawing.text(
        (10, 100), "Race: " + data['found_race'],
        font=current_font,
        fill=(255, 255, 255, 255))
    current_drawing.text(
        (10, 145), "Beauty: " +
        str(int(data['found_beauty'] * 100)) +
        "%",
        font=current_font,
        fill=(255, 255, 255, 255))

    step5 = image_file.convert('RGBA')
    step6 = Image.alpha_composite(step5, current_rect)
    final_image = Image.alpha_composite(step6, current_text)
    final_image.show()
    run_image_tool('image.jpg')
    return


def process_image(image_file):
    """
    Send image to Rekognize and return results.

    :param image_file: - The image file to process.
    :type image_file: str
    """
    post_request = requests.post(
        URL,
        data={
            'api_key': REKOGNITION_KEY,
            'api_secret': REKOGNITION_SECRET,
            'jobs': 'face_gender_race_age_beauty',
            'base64': b64encode(open(image_file, 'rb').read()),
        }
    )
    data = json.loads(post_request.text)
    return {
        'found_age': data['face_detection'][0]['age'],
        'found_race': str(data['face_detection'][0]['race'].keys()[0]),
        'found_beauty': data['face_detection'][0]['beauty'],
        'decided_sex': determine_sex(data['face_detection'][0]['sex'])
    }


def determine_sex(found_sex):
    """
    Determine sex from number returned by Rekognize.

    :param found_sex: - The number representing sex.
    :type image: int
    """
    if found_sex == 1:
        decided_sex = "male"
    elif found_sex == 0:
        decided_sex = "female"
    else:
        decided_sex = str(found_sex) + "% male"
    return decided_sex


def run_image_tool(image_file):
    """
    Run the Tool.

    :param image_file: - The image file to use.
    :type image: str
    """
    play_video(image_file)
    image_data = process_image(image_file)
    transformed_image = transform_image(image_file, image_data)
    display_image(transformed_image, image_data)
    return


run_image_tool('image.jpg')
