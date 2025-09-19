from platform import version

from prometheus_client import Counter,generate_latest  #counter: permite contar eventos, generate_last: genera todas las metricas en texto plano, Response: se usa para devolver el texto plano en FastPI
from fastapi.responses import Response
from fastapi import FastAPI
from api.routes import users


app = FastAPI(
    title="User API for Test Atomation",
    version ="1.0.0"
)

REQUEST_COUNTER = Counter("http_request_total","Total HTTP Requests",["method", "endpoint"])     #http_request_total: es el nombre de la metrica, Total HTTP requests: la descripcion, ["methode","endpoint"]: etiquetas para clasificar los datos (GET,POST etc)

#@app.middleware("http") :se ejecuta en cada request
@app.middleware("http")
async def prometheus_middleware(request,call_next):
    response = await call_next(request)  # call_next(request) llama al siguente componente (la ruta que pidio el usuario)
    REQUEST_COUNTER.labels(method=request.method, endpoint=request.url.path).inc()   # incrementa el contador con las etiquetas adecuadas
    return response


#esto expone todas las metricas recolectadas
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

app.include_router(users.router)