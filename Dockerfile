FROM ubuntu:focal

ENV TZ=UTC
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip git curl firefox firefox-geckodriver

RUN mkdir /opt/PWM-Police-Log-Downloader
RUN mkdir /output
WORKDIR /opt
#RUN git clone https://github.com/suidroot/PWM-Police-Log-Downloader.git PWM-Police-Log-Downloader
WORKDIR /opt/PWM-Police-Log-Downloader
COPY * /opt/PWM-Police-Log-Downloader/
RUN pip install -r requirments.txt
RUN chmod +x logdownloaderv2.py
#RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz | tar -C /usr/local/bin -zxvf -

ENV FILE_LOCATION=/output
ENTRYPOINT [ "/opt/PWM-Police-Log-Downloader/logdownloaderv2.py" ]
