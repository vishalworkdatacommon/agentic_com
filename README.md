# Agentic Commerce Solution POC

This project demonstrates an agentic commerce solution using Streamlit, a mock MCP (Merchant Center Platform) server, and Gemini for product discovery.

## Project Structure

- `mcp_server/`: Contains the mock MCP server implementation.
  - `main.py`: Flask application for the MCP server.
  - `products.json`: Sample product data.
  - `Dockerfile`: Dockerfile for the MCP server.
  - `requirements.txt`: Python dependencies for the MCP server.
- `streamlit_app/`: Contains the Streamlit application for the user interface.
  - `main.py`: Streamlit application entry point.
  - `Dockerfile`: Dockerfile for the Streamlit app.
  - `requirements.txt`: Python dependencies for the Streamlit app.
- `docker-compose.yml`: Docker Compose file for orchestrating the services.
- `README.md`: Project README file.

## Getting Started

### Running the Mock MCP Server Locally

1.  Navigate to the `mcp_server` directory:
    ```bash
    cd mcp_server
    ```
2.  Run the Flask application:
    ```bash
    python main.py
    ```
    The server will run on `http://127.0.0.1:5001`.

### Running the Streamlit Application Locally

1.  **Set your Gemini API Key:**
    Ensure you have your Google Gemini API key. You can set it as an environment variable:
    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    (Replace `YOUR_GEMINI_API_KEY` with your actual key.)
2.  Navigate to the project root directory (if you are not already there).
3.  Run the Streamlit application:
    ```bash
    streamlit run streamlit_app/main.py
    ```
    The Streamlit app will open in your web browser.

### Running with Docker Compose

1.  **Set your Gemini API Key:**
    Ensure you have your Google Gemini API key. You can set it as an environment variable in your shell session:
    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    (Replace `YOUR_GEMINI_API_KEY` with your actual key.)

2.  Navigate to the project root directory.

3.  Build and run the services using Docker Compose:
    ```bash
    docker compose up --build
    ```
    This will build the Docker images for both the MCP server and the Streamlit app, and then start them. The MCP server will be accessible on port 5001 and the Streamlit app on port 8501.

4.  To stop the services, press `Ctrl+C` in the terminal where Docker Compose is running, and then run:
    ```bash
    docker compose down
    ```

## Deployment to Google Cloud Run

This section provides instructions for deploying the MCP server and Streamlit app to Google Cloud Run. Ensure you have the `gcloud` CLI installed and authenticated, and a GCP project configured.

1.  **Set your GCP Project ID:**
    ```bash
    export GCP_PROJECT_ID="YOUR_GCP_PROJECT_ID"
    gcloud config set project $GCP_PROJECT_ID
    ```

2.  **Enable necessary GCP APIs:**
    ```bash
    gcloud services enable artifactregistry.googleapis.com run.googleapis.com
    ```

3.  **Build and Push MCP Server Docker Image to Artifact Registry:**
    ```bash
    gcloud auth configure-docker
    docker build -t us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest ./mcp_server
    docker push us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest
    ```

4.  **Deploy MCP Server to Cloud Run:**
    ```bash
    gcloud run deploy mcp-server \
      --image us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --port 5001 \
      --set-env-vars MCP_SERVER_URL="http://mcp-server.default.svc.run.app:5001" # Internal Cloud Run URL, will be updated later
    ```
    *Note: The `MCP_SERVER_URL` here is a placeholder for the internal Cloud Run service URL. You will need to update this once the MCP server is deployed and its actual URL is known.* Once deployed, get the service URL using `gcloud run services describe mcp-server --platform managed --region us-central1 --format 'value(status.url)'`.

5.  **Build and Push Streamlit App Docker Image to Artifact Registry:**
    ```bash
    docker build -t us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest ./streamlit_app
    docker push us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest
    ```

6.  **Deploy Streamlit App to Cloud Run:**
    ```bash
    export MCP_SERVER_PUBLIC_URL="$(gcloud run services describe mcp-server --platform managed --region us-central1 --format 'value(status.url)')"
    gcloud run deploy streamlit-app \
      --image us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --port 8501 \
      --set-env-vars GEMINI_API_KEY="YOUR_GEMINI_API_KEY",MCP_SERVER_URL="$MCP_SERVER_PUBLIC_URL"
    ```
    (Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.)