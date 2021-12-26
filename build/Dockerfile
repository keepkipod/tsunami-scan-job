FROM adoptopenjdk/openjdk13:debianslim

# Install dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/tsunami/repos

# Clone the plugins repo
RUN git clone --depth 1 "https://github.com/google/tsunami-security-scanner-plugins"

# Build plugins
WORKDIR /usr/tsunami/repos/tsunami-security-scanner-plugins/google
RUN chmod +x build_all.sh \
    && ./build_all.sh

RUN mkdir /usr/tsunami/plugins \
    && cp build/plugins/*.jar /usr/tsunami/plugins

# Compile the Tsunami scanner
WORKDIR /usr/repos/tsunami-security-scanner
COPY . .
RUN ./gradlew shadowJar \
    && cp $(find "./" -name 'tsunami-main-*-cli.jar') /usr/tsunami/tsunami.jar \
    && cp ./tsunami.yaml /usr/tsunami

# Stage 2: Release
FROM adoptopenjdk/openjdk13:debianslim-jre

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends nmap ncrack ca-certificates python3 python3-redis python3-pip python3-setuptools groff less \
    && pip3 install --upgrade pip \
    && apt-get clean

RUN pip3 --no-cache-dir install --upgrade awscli

WORKDIR /usr/tsunami
COPY --from=0 /usr/tsunami /usr/tsunami
COPY ./worker.py /usr/tsunami/worker.py
COPY ./rediswq.py /usr/tsunami/rediswq.py
COPY ./entrypoint.sh /usr/tsunami/entrypoint.sh

CMD  python3 worker.py