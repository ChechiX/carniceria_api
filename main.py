from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
conn = None

# Modelo de producto para la carnicería
class Producto(BaseModel):
    nombre: str
    tipo: str
    precio_kg: float
    stock_kg: float

# Conexión a Supabase al iniciar la app
@app.on_event("startup")
async def startup():
    global conn
    conn = await asyncpg.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await conn.close()

# GET - Listar productos
@app.get("/productos")
async def listar_productos():
    rows = await conn.fetch("SELECT * FROM productos")
    return [dict(row) for row in rows]

# POST - Agregar producto
@app.post("/productos")
async def agregar_producto(producto: Producto):
    await conn.execute(
        "INSERT INTO productos (nombre, tipo, precio_kg, stock_kg) VALUES ($1, $2, $3, $4)",
        producto.nombre, producto.tipo, producto.precio_kg, producto.stock_kg
    )
    return {"mensaje": "Producto agregado"}

# PUT - Actualizar producto
@app.put("/productos/{id}")
async def actualizar_producto(id: int, producto: Producto):
    result = await conn.execute(
        "UPDATE productos SET nombre=$1, tipo=$2, precio_kg=$3, stock_kg=$4 WHERE id=$5",
        producto.nombre, producto.tipo, producto.precio_kg, producto.stock_kg, id
    )
    return {"mensaje": "Producto actualizado"}

# DELETE - Eliminar producto
@app.delete("/productos/{id}")
async def eliminar_producto(id: int):
    await conn.execute("DELETE FROM productos WHERE id=$1", id)
    return {"mensaje": "Producto eliminado"}