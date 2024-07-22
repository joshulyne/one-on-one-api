from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from lib.agenda_lib import AgendaInput, download_agenda

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://one-on-one-ui.vercel.app",
    "https://one-on-one-ui.vercel.app/",
]

origin_regex = "http://(192|10)\.(168|10)\..*:3000"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/agenda")
def generate_agenda(agenda_input: AgendaInput):
    return download_agenda(agenda_input)
