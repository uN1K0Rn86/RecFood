# RecFood

## For the reviewer

The live deployment and the database are hosted by free providers, so if either of those is powered off / not working, please contact me.

## Links

- [Live deployment](https://recfood.fly.dev)
- [Technical report](https://github.com/uN1K0Rn86/RecFood/blob/main/technical_report.pdf)
- [Project canvas](https://github.com/uN1K0Rn86/RecFood/blob/main/project_canvas.pdf)

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
