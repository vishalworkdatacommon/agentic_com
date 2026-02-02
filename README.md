# AI-Powered Shopping Assistant

This is a demo of an AI-powered shopping assistant. You can ask it to find products for you, and it will use AI to understand what you're looking for and show you the most relevant items from its catalog.

## How to Run This Demo

This demo uses Docker, a tool that makes it easy to run applications in a self-contained environment.

### Prerequisites

*   **Docker:** You need to have Docker installed on your computer. You can download it from the [official Docker website](https://www.docker.com/products/docker-desktop/).
*   **Google Gemini API Key:** This project uses the Google Gemini AI model. You will need an API key to run it.
    *   You can get a Gemini API key from [Google AI Studio](https://makersuite.google.com/).

### Step 1: Set Your API Key

Before you start the application, you need to tell it what your Gemini API key is. You can do this by setting an "environment variable" in your terminal.

Open your terminal or command prompt and run the following command, replacing `"YOUR_GEMINI_API_KEY"` with the actual key you got from Google AI Studio:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### Step 2: Start the Application

1.  Make sure you are in the project's root directory in your terminal.
2.  Run the following command:

    ```bash
    docker compose up --build
    ```

    This will download all the necessary components, build the application, and start it. It might take a few minutes the first time you run it.

### Step 3: Use the Shopping Assistant

1.  Once the command in Step 2 is finished and you see a lot of text in your terminal, open your web browser.
2.  Go to the following address: `http://localhost:8501`
3.  You should now see the "Agentic Commerce Product Discovery" interface. Type what you're looking for into the search box (e.g., "a new phone" or "something for my smart home") and press Enter!

### How to Stop the Application

1.  Go back to the terminal where you ran the `docker compose up` command.
2.  Press `Ctrl + C` on your keyboard.
3.  Then, run the following command to clean up the containers:
    ```bash
    docker compose down
    ```

That's it! Enjoy your AI-powered shopping experience.
