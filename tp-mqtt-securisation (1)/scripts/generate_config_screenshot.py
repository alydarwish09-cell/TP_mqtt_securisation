from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_screenshot(title, content, output_path):
    width = 1000
    line_height = 24
    padding = 20
    lines = content.split('\n')
    height = (len(lines) + 2) * line_height + padding * 2
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
    except:
        font = ImageFont.load_default()
    draw.rectangle([0, 0, width, 40], fill=(50, 50, 50))
    draw.text((padding, 10), title, fill=(200, 200, 200), font=font)
    y = 60
    for line in lines:
        draw.text((padding, y), line, fill=(255, 255, 255), font=font)
        y += line_height
    img.save(output_path)

config_content = """# mosquitto.conf
allow_anonymous false
password_file /mosquitto/config/passwd
acl_file /mosquitto/config/acl

listener 1883
listener 8883
cafile /mosquitto/certs/ca.crt
certfile /mosquitto/certs/server.crt
keyfile /mosquitto/certs/server.key
require_certificate false"""

os.makedirs("/home/ubuntu/tp-mqtt-securisation/docs/images", exist_ok=True)
create_terminal_screenshot("mosquitto.conf - Security Configuration", config_content, "/home/ubuntu/tp-mqtt-securisation/docs/images/config_mosquitto.png")
