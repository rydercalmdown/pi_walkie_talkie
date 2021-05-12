FROM python:3.9
WORKDIR /code
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python-pyaudio \
    python3-pyaudio
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src .
ENTRYPOINT [ "python" ]
CMD [ "WalkieTalkieServer.py" ]
