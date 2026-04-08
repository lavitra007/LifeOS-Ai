# Stage 1: Build React Frontend
FROM node:18-alpine AS builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ ./
RUN npm run build

# Stage 2: Serve with FastAPI
FROM python:3.9-slim

WORKDIR /app

# Copy python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY server.py .

# Copy built React app from builder
COPY --from=builder /app/client/dist /app/client/dist

# Expose port
EXPOSE 8080

# Command to run
CMD ["python", "server.py"]
