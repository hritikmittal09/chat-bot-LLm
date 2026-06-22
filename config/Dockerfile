FROM ollama/ollama

WORKDIR /root

# copy entire config folder
COPY . /root/config

# create zera model
RUN ollama serve & \
    sleep 15 && \
    ollama create zera -f /root/config/Modelfile

    
EXPOSE 11434

CMD ["ollama", "serve"] 