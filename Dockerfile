# Stage 1: Build the frontend
FROM node:18 as frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend
FROM python:3.12-slim as backend-builder
WORKDIR /app

# Copy Poetry configuration from the root
COPY pyproject.toml poetry.lock README.md ./
RUN pip install poetry
RUN poetry install --no-root

# Copy the FastAPI app into the container
COPY .env.template .env
COPY pictoroute/ ./pictoroute
RUN poetry install

# Copy the built frontend files into the FastAPI static directory
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Set environment variables (if necessary)
ENV PORT=8000

# Run the FastAPI app with uvicorn
CMD ["poetry", "run", "uvicorn", "pictoroute.main:app", "--host", "0.0.0.0", "--port", "8000"]
