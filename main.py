import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from app import crud, schemas

app = FastAPI()

# Configuração para servir arquivos estáticos, como favicon
app.mount("/static", StaticFiles(directory="static"), name="static")

# Função para executar Trivy e retornar o resultado
def run_trivy_analysis():
    try:
        # Execute o comando Trivy
        result = subprocess.run(["trivy", "image", "your_image:tag"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Trivy Analysis</title>
        </head>
        <body>
            <h1>Trivy Analysis</h1>
            <form action="/run-analysis" method="post">
                <button type="submit">Run Trivy Analysis</button>
            </form>
            <div id="results"></div>
        </body>
    </html>
    """

@app.post("/run-analysis", response_class=HTMLResponse)
async def run_analysis():
    result = run_trivy_analysis()
    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Trivy Analysis Results</title>
        </head>
        <body>
            <h1>Trivy Analysis Results</h1>
            <pre>{result}</pre>
            <a href="/items">See Application</a>
        </body>
    </html>
    """)

@app.get("/items/", response_model=List[schemas.Item])
def read_items():
    return crud.get_items()

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int):
    item = crud.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate):
    return crud.create_item(item)

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate):
    updated_item = crud.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    success = crud.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}




