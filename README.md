# 🏦 Predicción de Riesgo Crediticio (Arquitectura Medallón)

Este proyecto académico implementa un modelo de Machine Learning para predecir la probabilidad de morosidad en clientes de tarjetas de crédito, integrando una base de datos en la nube con un entorno analítico en Python.

## ⚙️ Arquitectura del Proyecto
* **Capa Bronze (Datos Crudos):** Alojamiento de 33,377 registros históricos en Supabase.
* **Capa Silver (Datos Limpios):** Limpieza, estandarización y winsorización de valores atípicos mediante procedimientos almacenados (`Stored Procedures`) en SQL.
* **Capa Gold (Analítica Predictiva):** Entorno de Python conectado a la base de datos en tiempo real mediante API.

## 🧠 Resultados del Modelo Predictivo
* **Algoritmo utilizado:** Random Forest Classifier.
* **Precisión global del modelo:** 83.07%.
* **Hallazgos clave:** Al graficar el peso de las variables, el modelo determinó que el estado de pago del mes más reciente (`PAY_0`) y la línea de crédito otorgada (`LIMIT_BAL`) son los predictores financieros más fuertes de morosidad, superando al monto total de la deuda.
