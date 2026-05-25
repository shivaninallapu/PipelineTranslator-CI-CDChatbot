# Backend API

FastAPI backend service for the application.

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── routers/
│   ├── __init__.py
│   ├── chat.py          # Chat endpoints
│   └── health.py        # Health check
├── services/
│   ├── __init__.py
│   └── langchain_service.py  # Talks to Person 4's LangChain
├── models/
│   ├── __init__.py
│   └── schemas.py       # Request/response models
├── utils/
│   ├── __init__.py
│   └── file_handler.py  # File upload handling
├── .env                 # Environment variables (not in git)
├── .env.example         # Template for team
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your actual configuration values.

### Running the Application

1. **Start the development server from the repository root**
   ```bash
   source .venv311/bin/activate
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

   If you create your own virtual environment, activate that environment instead.

2. **Access the API**
   - API: http://localhost:8000
   - Interactive docs (Swagger): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

### API Endpoints

#### Health Check
- `GET /health` - Check if the service is running
- `GET /` - Root endpoint with basic info

#### Chat
- `POST /api/chat` - Send a chat message
  ```json
  {
    "message": "Hello, how can you help me?",
    "conversation_id": "conv-123"
  }
  ```

- `POST /api/chat/upload` - Upload a file for chat context
  - Form data with file upload

## Development

### Code Structure

- **Routers**: Handle HTTP requests and responses
- **Services**: Business logic and external service integration
- **Models**: Pydantic models for request/response validation
- **Utils**: Helper functions and utilities

### Integration with LangChain Service

The `langchain_service.py` file is set up to communicate with Person 4's LangChain implementation. Update the following in your `.env`:

```
LANGCHAIN_API_URL=http://localhost:8001
LANGCHAIN_API_KEY=your-api-key-here
```

### Testing

TODO: Add testing instructions

```bash
pytest
```

### Code Formatting

TODO: Set up code formatting

```bash
black .
flake8 .
```

## Environment Variables

See `.env.example` for all available environment variables.

## Team Notes

- Make sure to never commit `.env` to version control
- Always use `.env.example` as a template
- Update this README when adding new features or endpoints
- Coordinate with Person 4 for LangChain service integration

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `.env` or stop the other service
2. **Module not found**: Make sure you've activated the virtual environment and installed dependencies
3. **CORS errors**: Check `ALLOWED_ORIGINS` in `.env`

## License

TODO: Add license information
