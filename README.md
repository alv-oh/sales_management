# Sales Management

This project now supports both:
- The original CLI flow via `main.py` (unchanged)
- A modern React frontend connected to your existing Python modules via FastAPI

## Run The Existing CLI

1. Run `python main.py`

## Run The New Web UI (React + FastAPI)

1. Install backend dependencies:
	- `pip install fastapi uvicorn`
2. Start backend API from project root:
	- `uvicorn web_api:app --reload`
3. Open a second terminal and start frontend:
	- `cd frontend`
	- `npm install`
	- `npm run dev`
4. Open the URL shown by Vite (usually `http://localhost:5173`)

## Notes

- Existing module behavior is preserved. The new API calls functions from:
  - `products.py`
  - `customers.py`
  - `transactions.py`
  - `algorithms.py`
- The React app uses endpoint base URL `http://127.0.0.1:8000` by default.