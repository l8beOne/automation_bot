import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8009, reload=True)