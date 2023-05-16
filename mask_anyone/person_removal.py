import os
import subprocess
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
from E2FGVI.test import inpaint_video
from PIL import Image
from MAT.generate_image_modified import generate_images

from ultralytics import YOLO


def get_bboxes_yolo(video_path):
    model = YOLO("yolov8n.pt")
    results = model.predict(video_path, classes=0)
    boxes = []
    for result in results:
        boxes.append(result.boxes[0].xyxy)
    return boxes

def bboxes_to_masks(bboxes, video_path):
    print("Creating and saving masks from computed bboxes")
    vcap = cv2.VideoCapture(video_path)
    if vcap.isOpened(): 
        width = vcap.get(3)
        height = vcap.get(4)
    
    base_dir = os.path.join("data", "output", "masks")
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    for i, bbox in enumerate(bboxes):
        bbox = bbox.squeeze()
        mask = np.zeros((int(height), int(width)), dtype=np.uint8)
        mask[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])] = 255
        plt.imsave(os.path.join(base_dir, f"{i}.png"), mask, cmap='gray')
    return base_dir

def inpaint_e2fgvi(video_path, masks_path):
    out_path = inpaint_video(video_path, masks_path)

def inpaint_mat(video_path, masks_path):
    print("Starting inpaint")
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frames = []
    frame_dir = os.path.join("data", "output", "video_frames")
    out_path = os.path.join("data", "output", "result")
    while success:
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.save(os.path.join(frame_dir, f"{count}.png"))
        success, image = vidcap.read()
        count += 1
    generate_images("data/models/Places_512_FullData.pkl", frame_dir, masks_path, 512, 1, "const", out_path)
