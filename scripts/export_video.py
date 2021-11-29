import cv2
import sys
from pathlib import Path


def export_video(video_file: str, out_dir: str = "."):
    frame_nr = 0
    vidcap = cv2.VideoCapture(video_file)
    success, image = vidcap.read()
    while success:
        frame_str = str(frame_nr + 1).rjust(6, "0")
        filepath = Path(out_dir, frame_str[:2], frame_str[2:4], f'f-{frame_str}.jpg')
        # filepath.parent.mkdir(parents=True, exist_ok=True)
        print(filepath, cv2.imwrite(str(filepath), image, [cv2.IMWRITE_JPEG_QUALITY, 92, cv2.IMWRITE_JPEG_OPTIMIZE, 1]))
        frame_nr += 1
        success, image = vidcap.read()


video_file = sys.argv[1]
destination_folder = "."
if len(sys.argv) > 2:
    destination_folder = sys.argv[2]
print("Starting conversion of", video_file, "to", destination_folder)
export_video(video_file, destination_folder)
