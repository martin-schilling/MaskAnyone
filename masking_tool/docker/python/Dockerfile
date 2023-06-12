FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get -y install \
        python3 \
        python3-pip \
        python-is-python3 \
        python3-opencv \
        libgl1 \
        libglib2.0-0

RUN pip install \
    fastapi \
    mediapipe \
    uvicorn[standard] \
    ultralytics

RUN apt-get -y install git

RUN git clone https://github.com/geekyutao/Inpaint-Anything.git /Inpaint-Anything

RUN pip install torch torchvision torchaudio

RUN cd /Inpaint-Anything && pip install -e segment_anything

RUN pip install \
    pyyaml \
    tqdm \
    numpy \
    easydict==1.9.0 \
    #scikit-image==0.17.2 \
    scikit-image \
    scikit-learn==0.24.2 \
    opencv-python \
    tensorflow \
    joblib \
    matplotlib \
    pandas \
    albumentations==0.5.2 \
    hydra-core==1.1.0 \
    pytorch-lightning==1.2.9 \
    tabulate \
    kornia==0.5.0 \
    webdataset \
    packaging \
    scikit-learn==0.24.2 \
    wldhx.yadisk-direct
