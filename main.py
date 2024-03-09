from fastapi import FastAPI, Request
from starlette import status
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from url_storage import InMemoryStorage, DBStorage
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    storage_class: str = "IM"


settings = Settings()
app = FastAPI()

if settings.storage_class == "IM":
    URL_STORAGE = InMemoryStorage()
else:
    URL_STORAGE = DBStorage()

templates = Jinja2Templates(directory=".")


@app.get("/")
def read_root(request: Request):
    base_url = str(request.base_url)

    return templates.TemplateResponse("home.html", {"request": request,
                                                    "storage_type": settings.storage_class,
                                                    "base_url": base_url})

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


@app.get("/title")
def get_url_title(id: str):
    target_site = URL_STORAGE.get_site(id)
    if not target_site:
        return {"error": f"invalid id {id}"}

    return target_site.title
