import os
import mediapipe as mp
import cv2
import numpy as np

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

model_path = 'models/pose_landmarker_lite.task'

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the video mode:
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    output_segmentation_masks=True,
    num_poses=2)


def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image


def get_image_value(image):
    channel_sums = np.sum(image, axis=(0, 1)) / 255

    return channel_sums


def is_likely_frame_cut(image1, image2):
    channel_sum1 = get_image_value(image1)
    channel_sum2 = get_image_value(image2)

    # Check the difference for each channel
    differences = np.abs(channel_sum1 - channel_sum2) / channel_sum1

    # Check if any difference exceeds or equals 20%
    for difference in differences:
        if difference >= 0.2:
            return True

    return False


test_f = open('.ted_kid_pose.json', 'w')
test_f.write('[')



with PoseLandmarker.create_from_options(options) as landmarker:
    videoloc = "./videos/me2_cropcut.mp4"
    output_loc = "out.mp4"
    #videoloc = "./Input_Videos/Test_TED.mp4"
    #output_loc = "./Output_MaskedVideos/Test_TED.mp4"

    capture = cv2.VideoCapture(videoloc)

    frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)  # check frame width
    frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)  # check frame height
    samplerate = capture.get(cv2.CAP_PROP_FPS)
    capture = cv2.VideoCapture(videoloc)

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(output_loc, fourcc, fps = samplerate, frameSize = (int(frameWidth), int(frameHeight)))


    last_frame = None
    frame_counter = 0
    first = True

    while capture.isOpened():
        ret, frame = capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_timestamp_ms = capture.get(cv2.CAP_PROP_POS_MSEC)

            frame_counter += 1

            if last_frame is not None and is_likely_frame_cut(last_frame, frame):
                print('DETECT', frame_counter)
                landmarker = PoseLandmarker.create_from_options(options)

            last_frame = frame

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            if not first and self.frame_timestamp_ms == 0: # Fallback for videos with bad codec
                print("Can't properly process some frames - probably due to bad codec. Skipping Frame")
                continue

            pose_landmarker_result = landmarker.detect_for_video(mp_image, int(frame_timestamp_ms))

            output_image = cv2.cvtColor(mp_image.numpy_view(), cv2.COLOR_RGB2BGR)

            if pose_landmarker_result.segmentation_masks:
                print(len(pose_landmarker_result.pose_landmarks[0]))
                test_f.write('[')
                for landmark in pose_landmarker_result.pose_landmarks[0]:
                    #print('[', landmark.x, ',', landmark.y, ',', landmark.z, '],')
                    test_f.write('[' + str(landmark.x) + ', ' + str(landmark.y) + ', ' + str(landmark.z) + '],')
                test_f.write('],')
                continue
                for segmentation_mask in pose_landmarker_result.segmentation_masks:
                    mask = segmentation_mask.numpy_view()
                    seg_mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

                    output_image[seg_mask > 0.3] = 0

                    #interpolation_mask = (seg_mask > 0.05) & (seg_mask <= 0.4)
                    #interpolation_factor = (seg_mask - 0.05) / (0.4 - 0.05)
                    #output_image[interpolation_mask] = (1 - interpolation_factor[interpolation_mask]) * output_image[interpolation_mask] + interpolation_factor[interpolation_mask] * 0

                    #output_image = output_image.astype(float) * (1 - seg_mask) + np.zeros_like(output_image)
                    #output_image = output_image.astype(output_image.dtype)

                output_image = draw_landmarks_on_image(output_image, pose_landmarker_result)

            cv2.imshow('Video Frame', output_image)

            out.write(output_image)
            first = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Break the loop if no frames are left
            break

    out.release()
    capture.release()
    cv2.destroyAllWindows()

    test_f.write(']')
    test_f.close()
