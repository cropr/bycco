# copyright Chessdevil Consulting BVBA 2018 - 2020

from fastapi import HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import os.path
from bycco import app

@app.get('/')
def htmlroot():
    return RedirectResponse('/page')

@app.get('/page{path:path}')
def htmlpage(path: str):
    fn = os.path.join(os.path.dirname(__file__), 'page.html')
    try:
        with open(fn) as f:
            page = f.read()
        return HTMLResponse(page)
    except Exception:
        raise HTTPException(status_code=401, detail='page.html not found')


@app.get('/mgmt{path:path}')
def htmlmgmt(path:str):
    fn = os.path.join(os.path.dirname(__file__), 'mgmt.html')
    try:
        with open(fn) as f:
            page = f.read()
        return HTMLResponse(page)
    except Exception:
        raise HTTPException(status_code=401, detail='mgmt.html not found')
