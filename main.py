from typing import Union
from fastapi import FastAPI
from starlette import status
from fastapi.responses import RedirectResponse

from url_storage import Storage

app = FastAPI()
URL_STORAGE = Storage()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/store/")
def store_url(url: str):
    print(url)
    url_id = URL_STORAGE.process_url(url)
    return {"id": url_id}


@app.get("/statistics")
def statistics():
    stats_result = URL_STORAGE.get_statistics()
    return {"statistics": stats_result}


@app.get("/redirect")
def redirect_url(id):
    target_url = URL_STORAGE.get_redirect_url(id)
    if not target_url:
        return {"error": f"invalid id {id}"}

    return RedirectResponse(url=target_url, status_code=status.HTTP_302_FOUND)


@app.get("/get_title")
def redirect_url(id: str):
    target_site = URL_STORAGE.get_site(id)
    if not target_site:
        return {"error": f"invalid id {id}"}

    return target_site.title
