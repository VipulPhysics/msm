import serial
import struct

# Configure the UART connection
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

def receive_image():
    # Read the 4-byte image size header
    size_data = ser.read(4)
    if len(size_data) < 4:
        print("Failed to read image size")
        return None

    # Decode the size header
    image_size = struct.unpack('>I', size_data)[0]
    print(f"Image size: {image_size} bytes")

    # Read the image data
    image_data = ser.read(image_size)
    if len(image_data) < image_size:
        print("Incomplete image received")
        return None

    return image_data

def save_image(image_data, file_name):
    with open(file_name, 'wb') as f:
        f.write(image_data)
    print(f"Image saved as {file_name}")

try:
    count = 0
    while True:
        print("Waiting for image...")
        image_data = receive_image()
        if image_data:
            save_image(image_data, f"image_{count}.jpg")
            count += 1

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
