FROM ollama/ollama

WORKDIR /root

COPY . /root/config

RUN ollama serve & \
    sleep 15 && \
    ollama create zera -f /root/config/Modelfile

EXPOSE 11434

CMD ["serve"]