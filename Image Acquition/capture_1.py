import io, pygame, rpc, serial, serial.tools.list_ports, socket, struct, sys, time, os

# Fix Python 2.x compatibility.
try: 
    input = raw_input
except NameError: 
    pass

# Create a directory to save the images.
save_dir = "/home/pi/openmv_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print("\nAvailable Ports:\n")
for port, desc, hwid in serial.tools.list_ports.comports():
    print("{} : {} [{}]".format(port, desc, hwid))

sys.stdout.write("\nPlease enter a port name: ")
sys.stdout.flush()
interface = rpc.rpc_usb_vcp_master(port=input())
print("")
sys.stdout.flush()

def get_frame_buffer_call_back(pixformat_str, framesize_str, cutthrough, silent):
    if not silent: print("Getting Remote Frame...")

    result = interface.call("jpeg_image_snapshot", "%s,%s" % (pixformat_str, framesize_str))
    if result is not None:
        size = struct.unpack("<I", result)[0]
        img = bytearray(size)

        if cutthrough:
            result = interface.call("jpeg_image_read")
            if result is not None:
                interface.get_bytes(img, 5000)  # Fast data transfer.
        else:
            chunk_size = (1 << 15)  # 32KB chunks.
            if not silent: print(f"Reading {size} bytes...")
            for i in range(0, size, chunk_size):
                for j in range(3):  # Retry logic.
                    result = interface.call("jpeg_image_read", struct.pack("<II", i, chunk_size))
                    if result is not None:
                        img[i:i + chunk_size] = result
                        if not silent: print(f"{(i * 100) / size:.2f}% completed.")
                        break
                    if not silent: print(f"Retrying... {j + 1}/2")
                else:
                    if not silent: print("Error in transfer!")
                    return None

        return img
    else:
        if not silent: print("Failed to get Remote Frame!")
    return None

pygame.init()
screen_w, screen_h = 640, 480

try:
    screen = pygame.display.set_mode((screen_w, screen_h), flags=pygame.RESIZABLE)
except TypeError:
    screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption("Frame Buffer")
clock = pygame.time.Clock()

frame_count = 0  # To keep track of saved images.

while True:
    sys.stdout.flush()

    # Capture frame and get it as a byte array.
    img = get_frame_buffer_call_back("sensor.RGB565", "sensor.QQVGA", cutthrough=True, silent=True)
    if img is not None:
        try:
            # Display the captured frame.
            screen.blit(pygame.transform.scale(pygame.image.load(io.BytesIO(img), "jpg"), (screen_w, screen_h)), (0, 0))
            pygame.display.update()

            # Save the frame as a JPEG image on Raspberry Pi's SD card.
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{save_dir}/image_{timestamp}_{frame_count:04d}.jpg"
            with open(filename, "wb") as f:
                f.write(img)
                print(f"Image saved: {filename}")

            frame_count += 1  # Increment the frame counter.
            clock.tick()

        except pygame.error as e:
            print(f"Pygame Error: {e}")

    print(f"FPS: {clock.get_fps():.2f}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()