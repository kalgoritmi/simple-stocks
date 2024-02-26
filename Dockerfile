FROM python:3.12.2-slim-bullseye

RUN apt update \
    && apt install make -y --no-install-recommends \
    && apt clean

WORKDIR /project

COPY . .

RUN make env && make tests

ENV PATH="/project/venv/bin:$PATH"

CMD ["python", "main.py"]