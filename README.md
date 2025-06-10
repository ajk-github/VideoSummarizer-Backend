# EduSummarize Backend

A FastAPI service that:
1. Downloads audio from a YouTube URL  
2. Transcribes it with Whisper (with minute markers)  
3. Summarizes it using Gemini

---

## Prerequisites

- **Python 3.8+**  
- **FFmpeg** installed and on your PATH  
- **Google Gemini API Key**

---

## Setup

### Option 1: Quick Setup (Recommended)

Use the build script to automatically set up everything:

```bash
# Run the build script
python build.py
```

The build script will:
1. Check Python version
2. Verify FFmpeg installation
3. Create a virtual environment
4. Install dependencies
5. Run tests
6. Provide instructions for starting the server

### Option 2: Manual Setup
=======

1. **Clone the repo**  
    ```bash
    git clone https://github.com/depaulcdm/se491-project-edusummarize.git
    cd YourRepo/backend
    ```

2. **Create & activate a venv**  
    - **Windows CMD**  
      ```bat
      python -m venv venv
      .\venv\Scripts\activate
      ```  
    - **macOS/Linux**  
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install Python dependencies**  
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Configure your API key**  
    Create a file named `.env` in the `backend/` folder with:
    ```ini
    GEMINI_API_KEY=YOUR_GEMINI_DEVELOPER_API_KEY
    ```

5. **Running the Service**
  With your venv active and FFmpeg on PATH:
  ```bash
  uvicorn app.main:app --reload
  ```
---

## Testing with Postman

1. **Open Postman**  
   Launch the Postman app.

2. **Create a new request**  
   - Click **New** → **HTTP Request** or the **+** tab.

3. **Set up the request**  
   - **Method**: `POST`  
   - **URL**: `http://127.0.0.1:8000/process`

4. **Add headers**  
   | Key             | Value                   |
   | --------------- | ----------------------- |
   | Content-Type    | application/json        |

5. **Compose the body**  
   - Select the **Body** tab  
   - Choose **raw** and set the format dropdown to **JSON**  
   - Paste the following:
     ```json
     {
       "video_url": "https://www.youtube.com/watch?v=4QKIxObizXM"
     }
     ```

6. **Send the request**  
   Click **Send**.

7. **View the response**  
   You should see a JSON response similar to:
   ```json
   {
     "transcript": "[00:00]\nIn this video, we introduce the project scope...\n[01:00]\nNext, we dive into the architecture details...",
     "summary": "- [00:00] Introduction to project scope and objectives.\n- [01:00] Overview of the system architecture and components."

   }
   ```
## Development

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       ├── downloader.py
│       ├── summarizer.py
│       └── transcriber.py
├── test/
│   ├── test_downloader.py
│   ├── test_main.py
│   ├── test_summarizer.py
│   └── test_transcriber.py
├── .env
├── build.py
├── README.md
└── requirements.txt
```

### Running Tests

The build script automatically runs tests with coverage reporting. To run tests manually:

```bash
# Run all tests
python -m pytest test/ -v --cov=app

# Run specific test file
python -m pytest test/test_main.py -v

# Run tests with coverage report
python -m pytest test/ -v --cov=app --cov-report=term-missing
```
   }
