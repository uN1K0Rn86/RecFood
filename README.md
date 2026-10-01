# RecFood

## Development instructions

All instructions assume you are in the project root folder.

1. Install frontend dependencies:

- `cd frontend`
- `npm install`

2. Install backend dependencies:

- `cd backend`
- `poetry install`

3. Create .env in backend:

- `cd backend`
- `touch .env`
- Contents: `DATABASE_URL=<your-db-url>`

3. Run frontend:

- `cd frontend`
- `npm run dev`

4. Run backend:

- `cd backend`
- `poetry run uvicorn main:app --reload`
