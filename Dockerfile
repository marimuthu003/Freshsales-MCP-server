FROM python:3.12-slim
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml README.md ./

# Copy the source code
COPY src/ src/

# Install the package globally in the container
RUN pip install --no-cache-dir .

EXPOSE 8080

# Run the server
CMD ["python", "-m", "freshsales_mcp"]
