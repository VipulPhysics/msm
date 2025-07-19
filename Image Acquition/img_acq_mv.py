import sensor, image, pyb

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # Set camera to RGB mode
sensor.set_framesize(sensor.QVGA)    # Set the frame size to QVGA (320x240)
sensor.skip_frames(time=2000)        # Give the camera time to adjust

# Define color channels and thresholds for detection
color_channels = ['Red', 'Green', 'Blue', 'Yellow', 'Violet']
thresholds = {
    'Red': (150, 255, 0, 100, 0, 100),    # High Red, Low Green, Low Blue
    'Green': (0, 100, 150, 255, 0, 100),  # Low Red, High Green, Low Blue
    'Blue': (0, 100, 0, 100, 150, 255),   # Low Red, Low Green, High Blue
    'Yellow': (150, 255, 150, 255, 0, 100), # Red and Green combined, low Blue
    'Violet': (150, 255, 0, 100, 150, 255)  # Red and Blue combined, low Green
}

def is_color_match(img, threshold):
    """Check if the image predominantly matches the given threshold."""
    total_pixels = img.width() * img.height()
    match_count = 0

    for y in range(img.height()):
        for x in range(img.width()):
            r, g, b = img.get_pixel(x, y)
            if threshold[0] <= r <= threshold[1] and threshold[2] <= g <= threshold[3] and threshold[4] <= b <= threshold[5]:
                match_count += 1

    # If more than 60% of the image matches the threshold, it's a match
    return (match_count / total_pixels) * 100 > 60

def send_image_to_pi(img, color_name):
    """Send the image to Raspberry Pi via USB serial."""
    print(f"START:{color_name}")  # Indicate the start of the image data
    img.compressed(quality=90).to_bytes()  # Send compressed image data
    print("END")  # Indicate the end of the image data

previous_color = None  # Initialize the previous color as None

while True:
    for channel in color_channels:
        img = sensor.snapshot()

        # Check if the current image matches the color channel's threshold
        if is_color_match(img, thresholds[channel]):
            if channel != previous_color:
                send_image_to_pi(img, channel)
                previous_color = channel  # Update the previous color

    pyb.delay(1000)  # Small delay to avoid rapid detection
