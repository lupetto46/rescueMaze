import time
from keras.models import load_model
import cv2  # Install opencv-python
import numpy as np

print("Finished importing")


# 480, 620


def recognize(model, frame, class_names) -> str:
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image)
    prediction = np.argmax(prediction)
    return class_names[prediction]


def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


def get_center(frame: np.ndarray) -> tuple[int, int]:
    h, w, _ = frame.shape
    mh, mw = int(h / 2), int(w / 2)

    return mh, mw

    return frame[int(mh - mh / 2):int(mh + mh / 2), int(mw - mw / 2):int(mw + mh / 2)]


def color(frame, center: tuple):
    """Frame color must be BGR"""
    pixel = frame[center[0], center[1]]

    rr = pixel[2]
    gg = pixel[1]
    bb = pixel[0]
    return [bb, gg, rr]


def get_computations(model, frame, class_names) -> tuple[str, list[int, int, int]]:
    frame_letter = recognize(model, frame, class_names)

    center = get_center(frame)

    # color = unique_count_app(cv2.cvtColor(center, cv2.COLOR_BGR2RGB))

    return frame_letter


def get_max_position(bgr):
    maxval = np.max(bgr)
    somma = sum(bgr)
    print(somma)
    if somma < 100:
        return False
    for index, val in enumerate(bgr):
        if val == maxval and somma < 400:
            break
    else:
        return False

    for v in range(3):
        if v == index:
            bgr[v] = 255
        else:
            bgr[v] = 0
    return bgr


def main():
    print("Getting camera\s")
    camera1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    print("Finished getting camera")

    print("Loading model")
    model = load_model("model/keras_model.h5")
    print("Model loaded")

    print("Loading class names")
    with open("model/labels.txt", "r") as f:
        class_names = f.readlines()
        for class_name in class_names:
            class_names[class_names.index(class_name)] = class_name.split(" ")[1][:-1]
    print("Class names loaded: ", class_names)

    print("starting")
    font = cv2.FONT_ITALIC
    fps = 0
    kernel = np.zeros((420, 640, 3), np.uint8)
    while True:
        start = time.time()
        frame1 = camera1.read()[1]
        frame2 = camera2.read()[1]
        center2 = get_center(frame2)

        letter1 = get_computations(model, frame1, class_names)
        letter2 = get_computations(model, frame2, class_names)

        end = (time.time() - start) * 1000
        try:
            fps = int((25 * 40) / end)
        except ZeroDivisionError:
            fps = 0

        frame1 = cv2.putText(frame1, letter1, (150, 50), font, 1, (255, 0, 0), 2)
        frame2 = cv2.putText(frame2, letter2, (150, 50), font, 1, (255, 0, 0), 2)
        frame1 = cv2.putText(frame1, str(fps), (50, 50), font, 1, (255, 0, 0), 2)
        frame2 = cv2.putText(frame2, str(fps), (50, 50), font, 1, (255, 0, 0), 2)

        # Color of center pixel
        frame2_color: list[int, int, int] = color(frame2, get_center(frame2))
        cv2.rectangle(frame2, center2[::-1], center2[::-1], (255, 255, 0), 2)
        #print("Frame color", frame2_color)
        bgr_extreme = get_max_position(frame2_color)

        print(bgr_extreme)

        kernel[:] = bgr_extreme

        cv2.imshow("color found", kernel)
        cv2.imshow("frame1", frame1)
        cv2.imshow("frame2", frame2)

        # print(f"Frames completed in: {round(end, 2)}ms = {fps}fps")
        key = cv2.waitKey(1)
        if key == ord("q"):
            cv2.destroyAllWindows()
            return


if __name__ == '__main__':
    main()
