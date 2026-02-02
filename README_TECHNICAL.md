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
    gcloud services enable artifactregistry.googleapis.com run.googleapis.com secretmanager.googleapis.com firestore.googleapis.com
    ```

3.  **Manual Prerequisite: Create Firestore Database (Project Owner required):**
    Due to strict IAM policies, you might need a Project Owner to execute this command:
    ```bash
    gcloud firestore databases create --location=us-central --type=firestore-native --project="$GCP_PROJECT_ID"
    ```
    Confirm the database is created before proceeding.

4.  **Create a Secret for the Gemini API Key:**
    ```bash
    # Create the secret container
    gcloud secrets create gemini-api-key --replication-policy="automatic"

    # Add your API key as a secret version
    printf "YOUR_GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=- 
    ```
    (Replace `YOUR_GEMINI_API_KEY` with your actual key.)

5.  **Manual Prerequisite: Create Service Accounts and Grant Permissions (Project Owner required for policy binding):**
    *   **For Streamlit App (Accessing Secret Manager):**
        ```bash
        gcloud iam service-accounts create streamlit-app-sa --display-name "Streamlit App Service Account"
        gcloud secrets add-iam-policy-binding gemini-api-key \
          --member "serviceAccount:streamlit-app-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
          --role "roles/secretmanager.secretAccessor"
        ```
    *   **For MCP Server (Accessing Firestore):**
        ```bash
        gcloud iam service-accounts create mcp-server-sa --display-name "MCP Server Service Account"
        gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
          --member "serviceAccount:mcp-server-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com" \
          --role "roles/datastore.user"
        ```
    Confirm both Service Accounts are created and have the correct roles before proceeding.

6.  **Build and Push MCP Server Docker Image to Artifact Registry:**
    ```bash
    gcloud auth configure-docker
    docker build -t us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest ./mcp_server
    docker push us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest
    ```

7.  **Deploy MCP Server to Cloud Run:**
    ```bash
    gcloud run deploy mcp-server \
      --image us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/mcp-server:latest \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --port 5001 \
      --service-account mcp-server-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com
    ```

8.  **Build and Push Streamlit App Docker Image to Artifact Registry:**
    ```bash
    docker build -t us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest ./streamlit_app
    docker push us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest
    ```

9.  **Deploy Streamlit App to Cloud Run with the Service Account:**
    ```bash
    # Get the URL of the deployed MCP server
    export MCP_SERVER_PUBLIC_URL="$(gcloud run services describe mcp-server --platform managed --region us-central1 --format 'value(status.url)')"

    gcloud run deploy streamlit-app \
      --image us-central1-docker.pkg.dev/$GCP_PROJECT_ID/ucp-repo/streamlit-app:latest \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --port 8501 \
      --service-account streamlit-app-sa@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
      --set-env-vars MCP_SERVER_URL="$MCP_SERVER_PUBLIC_URL",GCP_PROJECT="$GCP_PROJECT_ID"
    ```