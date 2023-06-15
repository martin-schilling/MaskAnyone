FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ninja-build \
    python3-pip

RUN apt install -y git

RUN git clone https://github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model.git
WORKDIR /Thin-Plate-Spline-Motion-Model
RUN pip install -r requirements.txt

RUN mkdir checkpoints \
    && wget -c https://cloud.tsinghua.edu.cn/f/da8d61d012014b12a9e4/?dl=1 -O checkpoints/vox.pth.tar

ENTRYPOINT ["python3", "/Thin-Plate-Spline-Motion-Model/demo.py"]