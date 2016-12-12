FROM python:2-wheezy

ENV pydir /usr/src/app
ENV vokaturidir ${pydir}/VokaturiAudio
ENV rabbitport 5672

RUN apt-get update && apt-get install -y portaudio19-dev
RUN mkdir -p ${pydir}

ADD . ${pydir}

RUN cd ${vokaturidir} && pip install -r requirements.txt

WORKDIR ${vokaturidir}/lib

RUN pwd

ENTRYPOINT ./main.py rabbit ${rabbitport}
