# PromptLab

**Your AI Prompt Engineering Platform**

---

## Project Overview and Purpose

PromptLab is an internal tool designed for AI engineers to store, organize, and manage their prompts efficiently. It acts as a "Postman for Prompts," providing a centralized workspace for teams to enhance AI workflows with clear template management, prompt categorization, and performance tracking.

---

## Features

- Store prompt templates with variables (`{{input}}`, `{{context}}`)
- Organize prompts into collections
- Tag and search prompts
- Track version history
- Test prompts with sample inputs

---

## Project Structure

```
promptlab/
├── README.md                    # Documentation
├── PROJECT_BRIEF.md             # Assignment details
├── GRADING_RUBRIC.md            # Assessment criteria
│
├── backend/
│   ├── app/
│   └── tests/
│   ├── main.py                 # Entry point
│   └── requirements.txt
│
├── frontend/                    # Frontend to be added
├── docs/                        # Documentation resources
└── .github/                     # CI/CD configurations
```

---

## Prerequisites and Installation

### Prerequisites

- **Python 3.10+**: Make sure Python is installed on your machine.
- **Node.js 18+**: Required for the frontend in later development phases.
- **Git**: Version control system.

### Installation

1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd promptlab
```

2. **Backend Setup**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

---

## Quick Start Guide

- **Run the Application Locally**

```bash
cd backend
python main.py
```

- **Access API**

  - API Base URL: `http://localhost:8000`
  - API Documentation: `http://localhost:8000/docs`

---

## API Endpoint Summary with Examples

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API health |
| GET | `/prompts` | List all prompts |
| GET | `/prompts/{id}` | Retrieve a single prompt |
| POST | `/prompts` | Create a new prompt |
| PUT | `/prompts/{id}` | Update an existing prompt |
| DELETE | `/prompts/{id}` | Delete a prompt |
| GET | `/collections` | List all collections |
| GET | `/collections/{id}` | Retrieve collection details |
| POST | `/collections` | Create a new collection |
| DELETE | `/collections/{id}` | Remove a collection |

---

## Development Setup Instructions

Ensure Python, Node.js, and Git are installed. Set up the backend as described, and ensure Docker and GitHub Actions are installed for CI/CD setup, planned in upcoming development phases.

---

## Contributing Guidelines

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/feature-name`.
5. Open a pull request.

---

## Support

For issues, check the `PROJECT_BRIEF.md` file, the `GRADING_RUBRIC.md`, or ask questions in the course forum.

---

**Welcome to the team! We look forward to your contributions to pioneering prompt management for AI engineering. 🚀**
