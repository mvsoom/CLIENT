import base64
import json
from io import BytesIO
import cv2
import requests
from PIL import Image


IMAGE_INPUT_SIZE = (336, 336)
WORKER_ADDR = 'http://localhost:40000'
HEADERS = {'User-Agent': 'LLaVA Client'}
TIMEOUT = 20 # seconds

MODEL = 'LLaVA-Lightning-MPT-7B-preview'
TEMPERATURE = 0.2
MAX_NEW_TOKENS = 512
STOP_TOKENS = ['\n', '<|im_end|>']


def encode_image(image: Image.Image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_b64_str = base64.b64encode(buffered.getvalue()).decode()
    return img_b64_str


def process_frame(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = image.resize(IMAGE_INPUT_SIZE)
    return image


def encode_frame(frame):
    image = process_frame(frame)
    encoded_frame = encode_image(image)
    return encoded_frame


def describe(frame):
    prompt = '<|im_start|><image>The'
    encoded_frame = encode_frame(frame)

    pload = {
        'model': MODEL,
        'prompt': prompt,
        'temperature': TEMPERATURE,
        'max_new_tokens': MAX_NEW_TOKENS,
        'stop': STOP_TOKENS,
        'images': [encoded_frame],
    }

    response = requests.post(
        url=WORKER_ADDR + '/worker_generate',
        headers=HEADERS,
        json=pload,
        timeout=TIMEOUT
    )
    output = json.loads(response.text)

    description = 'The ' + output
    return description