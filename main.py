from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from short_link.models import Link
from short_link.db import Base, engine
from short_link.builder_short_link import build_short_link, get_domain_name

app = FastAPI(title="short links")
Base.metadata.create_all(bind=engine)


@app.get(
    "/",
    response_description="Hello",
    description="info",
)
async def get():
    return 'Please read /docs'


@app.post(
    "/create",
    response_description="Added a original link and return short link",
    description="Added a original link and create return link",
)
async def create(request: Request):
    original_link = await request.json()
    original_link = get_domain_name(original_link['link'])
    short_postfix = Link.add_link(original_link=original_link)
    short_link = build_short_link(short_postfix, url=request.base_url)
    return short_link


@app.get(
    "/{short_postfix}",
    response_description="Redirect to original link",
    description="Redirect to original link",
    response_class=RedirectResponse,
    status_code=307
)
async def redirect_to_original_link(short_postfix: str):
    original_link = Link.get_original_link(short_postfix)
    return 'https://' + original_link
