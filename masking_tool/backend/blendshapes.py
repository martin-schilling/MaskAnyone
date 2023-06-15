import os
import mediapipe as mp
import cv2

def extract_blendshapes(video_name):
    model_path = os.path.join("models", "face_landmarker.task")
    video_path = os.path.join("videos", video_name)

    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1)
    
    blendshapes = []

    with FaceLandmarker.create_from_options(options) as landmarker:
        capture = cv2.VideoCapture(video_path)
        samplerate = capture.get(cv2.CAP_PROP_FPS)
        print("aaaaaaaaaa", samplerate)

        first = True
        while capture.isOpened():
            ret, frame = capture.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_timestamp_ms = capture.get(cv2.CAP_PROP_POS_MSEC)

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                if not first and frame_timestamp_ms == 0: # Fallback for videos with bad codec
                    print("Bad coded probably - can't properly processsome frames")
                    continue

                face_landmarker_result = landmarker.detect_for_video(mp_image, int(frame_timestamp_ms))
                if len(face_landmarker_result.face_blendshapes):
                    # Currently only working for one face, since all other faces are not added
                    processed_landmarkers = {entry.category_name: entry.score for entry in face_landmarker_result.face_blendshapes[0]}
                    blendshapes.append(processed_landmarkers)
                else:
                    print("no face detected, using last result for consistency")
                    blendshapes.append(blendshapes[len(blendshapes)-1])

                first = False
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        capture.release()
    return blendshapes