FROM python:3.11

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  POETRY_VERSION=1.3.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /itmo_coffee_project/
COPY . /itmo_coffee_project
WORKDIR /itmo_coffee_project

# Project initialization:
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python", "-m", "app"]

