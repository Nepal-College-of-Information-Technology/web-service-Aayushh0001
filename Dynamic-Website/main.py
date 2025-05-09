from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB, Query
from fastapi.staticfiles import StaticFiles

app = FastAPI()
db = TinyDB("db.json")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    items = db.all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add")
async def add_item(item: str = Form(...)):
    db.insert({"item": item})
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{item_id}")
async def delete_item(item_id: int):
    db.remove(doc_ids=[item_id])
    return RedirectResponse("/", status_code=303)

@app.post("/edit/{item_id}")
async def edit_item(item_id: int, new_item: str = Form(...)):
    db.update({"item": new_item}, doc_ids=[item_id])
    return RedirectResponse("/", status_code=303)

