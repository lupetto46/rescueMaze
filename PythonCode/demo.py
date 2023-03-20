import CameraLib

while True:
    try: 
        print(CameraLib.get_color_sx())
    except KeyboardInterrupt:
        print("Stopped by user")
        break