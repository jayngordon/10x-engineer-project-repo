# PromptLab Frontend

A React frontend powered by Vite that connects to the PromptLab FastAPI backend.

## Prerequisites
- Node.js 18+ (npm bundled)
- Backend running on `http://localhost:8080` (configurable).

## Getting started
```bash
cd frontend
npm install
npm run dev
```

This starts the Vite dev server (default `http://localhost:5173`). The front-end reads the backend base URL from the `VITE_API_BASE_URL` environment variable. You can override it by creating a `.env.local` or by running:
```bash
VITE_API_BASE_URL=http://localhost:8080 npm run dev
```

## Building for production
```bash
npm run build
npm run preview
```

The `frontend` directory is self-contained, so you can build assets separately or integrate the output with Docker later.
