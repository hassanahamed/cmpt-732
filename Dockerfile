FROM python:3.7
COPY . /
WORKDIR /
RUN pip3 install -r src/requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-11-jre-headless \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "--theme.base=dark"]

CMD ["src/app.py"]

