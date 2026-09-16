# Stage 1: Build the React application
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy frontend package.json
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy frontend source and build
COPY frontend/ ./
RUN rm -f .env && npm run build

# Stage 2: Build the FastAPI backend
FROM python:3.11-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose port (Render sets PORT env variable dynamically, default to 10000 here)
ENV PORT=10000
EXPOSE $PORT

# Start the application
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"]
