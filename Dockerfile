FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel
RUN pip install uv

RUN apt update && \
    apt install -y espeak-ng ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/Zyphra/Zonos.git .
RUN uv pip install --system -e . && uv pip install --system -e .[compile]

COPY . ./

EXPOSE 7861