from . import audit_logger
from .audit_logger_formatter import CustomFormatter
import random
import uvicorn
import json
from fastapi import FastAPI, Query, Request, Response, status, HTTPException
from fastapi.responses import FileResponse
from http import HTTPStatus
from starlette.background import BackgroundTask

logfile = "./app/log/audit.log"

app = FastAPI()
favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

formatter = CustomFormatter('%(asctime)s')
logger = audit_logger.get_logger(__name__, formatter)
status_reasons = {x.value:x.name for x in list(HTTPStatus)}

def get_req(request: Request, response: Response):
    return {'req': {
        'url': request.url.path,
        'query': request.query_params.get("word")
        },
        'res': {'statusCode': response.status_code, 'body': {'statusCode': response.status_code,
                   'status': status_reasons.get(response.status_code)}}}

def write_log_data(request, response):
    logger.info(request.method + ' ' + request.url.path, extra={'extra_info': get_req(request, response)})

@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    response.background = BackgroundTask(write_log_data, request, response)
    return response

@app.get("/api/jumble/")
async def read_word(word: str | None = Query(default=None, min_length=2, regex="^[a-zA-Z]+$" )):
            # check if the sting is not composed of the same character
            def allCharactersSame(s) :
                n = len(s)
                for i in range(1, n) :
                    if s[i] != s[0] :
                        return False
                return True

            s = word
            if allCharactersSame(s) :
                raise HTTPException(status_code=404, detail="Try a word insteed :)")
                return
            else :
                while True:
                    random_word = random.sample(word, len(word))
                    jumbled = ''.join(random_word)
                    if (jumbled != word):
                        jumbled = jumbled.lower()
                        return {"jumbled_word": jumbled}
                    else:
                        continue

@app.get("/api/audit")
def read_log(request: Request):
    n = 10
    with open(logfile) as f:
        data = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")
    return (data[-n:])



