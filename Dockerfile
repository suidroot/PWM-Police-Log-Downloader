FROM ubuntu:noble

ENV TZ=UTC
ENV DEBIAN_FRONTEND=noninteractive

# Install Firefox from Mozilla's apt repo (Noble's apt firefox is a snap wrapper and doesn't work in Docker)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip python3-venv git curl ca-certificates && \
    install -d -m 0755 /etc/apt/keyrings && \
    curl -fsSL https://packages.mozilla.org/apt/repo-signing-key.gpg | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" > /etc/apt/sources.list.d/mozilla.list && \
    printf 'Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1001\n' > /etc/apt/preferences.d/mozilla-firefox && \
    apt-get update && \
    apt-get install -y firefox libdbus-glib-1-2 libgtk-3-0t64 libxt6t64

RUN mkdir -p /opt/PWM-Police-Log-Downloader /output && \
    chown 1000:1000 /opt/PWM-Police-Log-Downloader

WORKDIR /opt/PWM-Police-Log-Downloader
COPY --chown=1000:1000 * /opt/PWM-Police-Log-Downloader/

RUN python3 -m venv /opt/venv && chown -R 1000:1000 /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirments.txt

RUN chmod +x logdownloaderv2.py
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz | tar -C /usr/local/bin -zxvf -

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV FILE_LOCATION=/output
ENTRYPOINT [ "/entrypoint.sh" ]