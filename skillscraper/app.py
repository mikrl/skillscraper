from fastapi import FastAPI
import redis

from skillscraper.search import IndeedSearch

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/search/{title}")
async def lookup(title: str):
    # raise Exception
    indeed = IndeedSearch()
    response = indeed.do_search2022(title, "Listowel, ON")
    return {"Body": response.content}
