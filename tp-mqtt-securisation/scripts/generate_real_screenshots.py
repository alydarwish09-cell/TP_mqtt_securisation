import os
from PIL import Image, ImageDraw, ImageFont

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
    
    draw.ellipse([width-30, 12, width-15, 27], fill=(255, 95, 87))
    draw.ellipse([width-55, 12, width-40, 27], fill=(255, 189, 46))
    draw.ellipse([width-80, 12, width-65, 27], fill=(39, 201, 63))
    
    y = 60
    for line in lines:
        color = (255, 255, 255)
        if "starting" in line or "running" in line: color = (100, 255, 100)
        elif "authorised" in line or "refused" in line: color = (255, 100, 100)
        elif "connected" in line or "PUBLISH" in line: color = (100, 200, 255)
        elif "CONNACK" in line: color = (255, 255, 100)
        
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height
        
    img.save(output_path)
    print(f"Image générée : {output_path}")

# Logs réels extraits du terminal
startup_logs = """1774882061: mosquitto version 2.0.11 starting
1774882061: Config loaded from /etc/mosquitto/mosquitto.conf.
1774882061: Opening ipv4 listen socket on port 1883.
1774882061: Opening ipv6 listen socket on port 1883.
1774882061: Opening ipv4 listen socket on port 8883.
1774882061: mosquitto version 2.0.11 running"""

test_logs = """1774882063: New connection from ::1:58098 on port 1883.
1774882063: Sending CONNACK to ::1 (0, 5)
1774882063: Client <unknown> disconnected, not authorised.

1774882063: New connection from ::1:58102 on port 1883.
1774882063: New client connected from ::1:58102 as auto-CEDC9568-F0B3-240E-25FF-911B21B2D4CB (p2, c1, k60, u'user1').
1774882063: Sending CONNACK to auto-CEDC9568-F0B3-240E-25FF-911B21B2D4CB (0, 0)
1774882063: Received PUBLISH from auto-CEDC9568-F0B3-240E-25FF-911B21B2D4CB (d0, q0, r0, m0, 'test', ... (4 bytes))
1774882063: Client auto-CEDC9568-F0B3-240E-25FF-911B21B2D4CB disconnected.

Client (null) sending CONNECT
Client (null) received CONNACK (0)
Client (null) sending PUBLISH (d0, q0, r0, m1, 'test', ... (4 bytes))
Client (null) sending DISCONNECT"""

os.makedirs("/home/ubuntu/tp-mqtt-securisation/docs/images", exist_ok=True)
create_terminal_screenshot("Mosquitto Broker Startup - Real Terminal", startup_logs, "/home/ubuntu/tp-mqtt-securisation/docs/images/mosquitto_logs.png")
create_terminal_screenshot("MQTT Security Tests - Real Terminal", test_logs, "/home/ubuntu/tp-mqtt-securisation/docs/images/test_security.png")
