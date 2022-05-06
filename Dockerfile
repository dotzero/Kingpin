FROM python:3.9-buster

WORKDIR /build
ADD . /build

RUN apt-get update && apt-get install -y -q --no-install-recommends \
    build-essential \
    libfontconfig1-dev \
    libfreetype6-dev \
    $jpeg \
    libpng-dev \
    $ssl \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    python \
    zlib1g-dev \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf https://wkhtmltopdf.org/downloads.html
RUN wget -nv -O /tmp/wkhtmltopdf.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    dpkg -i /tmp/wkhtmltopdf.deb && \
    cp /usr/local/bin/wkhtmltopdf /usr/bin/ && \
    cp /usr/local/bin/wkhtmltoimage /usr/bin/ && \
    rm /tmp/wkhtmltopdf.deb

# Install app requirements
RUN pip install -r /build/requirements.txt

CMD [ "make", "files" ]
