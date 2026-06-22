FROM python:3.11-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

# copy dependency files first
COPY pyproject.toml .
COPY uv.lock .

# install dependencies
RUN uv sync --frozen

# copy whole project
COPY . .

# streamlit port
EXPOSE 8501

# environment
ENV PYTHONUNBUFFERED=1

# run app
CMD ["uv", "run", "streamlit", "run", "Gui.py", "--server.address=0.0.0.0", "--server.port=8501"]