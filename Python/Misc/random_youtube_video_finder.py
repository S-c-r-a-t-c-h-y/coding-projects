import random
import requests


size = 11
base_url = "https://www.youtube.com/watch?v="

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = lowercase.upper()

digits = "0123456789"
symbols = "-_"

all_chars = lowercase + uppercase + digits + symbols


def generate_random_sequence(elems=all_chars, size=size):
    return "".join(random.choices(elems, k=size))


def generate_random_url():
    return base_url + generate_random_sequence()


def is_valid_youtube_url(url):
    checker_url = f"https://www.youtube.com/oembed?url={url}"

    request = requests.get(checker_url)

    return request.status_code == 200


url = generate_random_url()
while not is_valid_youtube_url(url):
    url = generate_random_url()

print(url)
