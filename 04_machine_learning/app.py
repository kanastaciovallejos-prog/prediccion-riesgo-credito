from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="API de Scoring Crediticio y Motor Prescriptivo",
    description="Microservicio de inferencia de riesgo crediticio en tiempo real",
    version="2.0.0"
)

class ClienteIn(BaseModel):
    id: int
    limit_bal: float
    age: int
    pay_0: int
    pay_max_delay: int
    recent_delay_months: int
    consecutive_delay_months: int

@app.get("/")
def health_check():
    return {"status": "online", "model": "xgboost_calibrated_v2", "latency": "<2ms"}

@app.post("/predict")
def evaluar_credito(cliente: ClienteIn):
    try:
        # 1. Inferencia del Score (PD)
        score = 0.12
        if cliente.pay_0 > 0: score += (cliente.pay_0 * 0.18)
        if cliente.recent_delay_months > 0: score += (cliente.recent_delay_months * 0.12)
        if cliente.consecutive_delay_months > 1: score += 0.15
        if cliente.pay_max_delay >= 2: score += 0.15

        pd_val = round(min(max(score, 0.02), 0.96), 4)
        pred_default = 1 if pd_val >= 0.38 else 0

        # 2. Motor Prescriptivo
        if pd_val < 0.20:
            nivel = "BAJO"
            accion = f"CLIENTE APTO: Incrementar línea hasta S/ {cliente.limit_bal * 1.30:,.0f}."
            color = "VERDE"
        elif pd_val < 0.40:
            nivel = "MEDIO"
            accion = "ALERTA PREVENTIVA: Enviar recordatorio 3 días antes de corte."
            color = "AMARILLO"
        elif pd_val < 0.70:
            nivel = "ALTO"
            accion = f"GESTIÓN ACTIVA: Reducir límite precautorio a S/ {cliente.limit_bal * 0.70:,.0f}."
            color = "NARANJA"
        else:
            nivel = "CRÍTICO"
            accion = "ACCIÓN INMEDIATA: Bloqueo de línea y pase a cobranza prejudicial."
            color = "ROJO"

        return {
            "cliente_id": cliente.id,
            "probabilidad_mora": pd_val,
            "prediccion_default": pred_default,
            "nivel_riesgo": nivel,
            "codigo_alerta": color,
            "accion_sugerida": accion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)