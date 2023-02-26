import uvicorn

if __name__ == '__main__':

    uvicorn.run("src.core.app:app", host='localhost', port=8000)
