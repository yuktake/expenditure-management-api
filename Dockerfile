FROM python:3.11

WORKDIR /app

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python -
# Poetryのパスの設定
ENV PATH /root/.local/bin:$PATH
# Poetryが仮想環境を生成しないようにする
RUN poetry config virtualenvs.create false

COPY ./app/ .
RUN poetry install

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]