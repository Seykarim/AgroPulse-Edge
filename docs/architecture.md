# Arquitectura Técnica - AgroPulse Edge

```text
    [ LOTE 1: CAFÉ ]              [ LOTE 2: PLÁTANO ]            [ LOTE 3: GANADERÍA ]
  Nodo Suelo/Clima (ESP32)      Nodo Suelo/Clima (ESP32)       Nodo Calidad Pastos (ESP32)
         │                             │                                │
         └─────────────────────────────┼────────────────────────────────┘
                                       │ (Enlace LoRa 915 MHz / Mesh)
                                       ▼
                          ┌──────────────────────────┐
                          │   GATEWAY CENTRAL FINCA  │
                          │   (Almacenamiento Local) │
                          └────────────┬─────────────┘
                                       │
                      ┌────────────────┴────────────────┐
                      ▼                                 ▼
         [ Alerta SMS / WhatsApp ]           [ Servidor Nube / API DaaS ]
         (Para el Productor)                 (Cooperativas / Gremios)
---

#### 8. README Principal (`README.md`)

```bash
cat << 'EOF' > README.md
# 🌾 AgroPulse Edge — Telemetría Agrícola & IA en el Borde para el Agro Colombiano

[![Hardware](https://img.shields.io/badge/Hardware-ESP32--S3%20%2F%20LoRa%20915MHz-red.svg)](#hardware)
[![Edge AI](https://img.shields.io/badge/Edge%20AI-TinyML%20%2F%20Scikit--Learn-green.svg)](#edge-ai)
[![Region](https://img.shields.io/badge/Region-Colombia%20%2F%20LatAm-yellow.svg)](#cobertura)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> *"Inteligencia agrícola y ganadera autónoma: telemetría de precisión sin dependencia de internet en el lote."*

**AgroPulse Edge** es un sistema modular de bajo costo diseñado para optimizar la producción agrícola y ganadera en Colombia. Combina sensores de humedad de suelo (NPK), monitoreo de microclima, radiofrecuencia de largo alcance **LoRaWAN** e **Inteligencia Artificial en el Borde (TinyML)** para predecir el estrés hídrico de las plantas y prevenir brotes de fitopatógenos (como la Roya en el café o la Sigatoka en el plátano).

---

## 🌟 Características Clave

- **Operación 100% Offline (Red en Malla LoRaWAN):** Conexión estable entre lotes a más de 8 km de distancia sin requerir cobertura celular.
- **Predicción de Riesgo Epidemiológico:** Un modelo TinyML local analiza la combinación de temperatura y humedad para alertar sobre la aparición de hongos antes de la manifestación visible.
- **Eficiencia en Fertirriego:** Monitoreo continuo de NPK y conductividad del suelo para evitar la sobrefertilización y reducir costos operativos.
- **Energía Solar Autónoma:** Nodos alimentados por micro-paneles solares y baterías Li-Ion con consumo inferior a 0.8 Watts.
- **Alertas Accesibles:** Notificaciones inteligentes enviadas vía SMS, WhatsApp o interfaz gráfica para pequeños y medianos productores.

---

## 📁 Estructura del Repositorio

```text
AgroPulse-Edge/
├── README.md               # Presentación general
├── LICENSE                 # Licencia libre MIT
├── .gitignore
├── firmware/               # Código C++ PlatformIO para ESP32-S3
│   ├── src/main.cpp
│   └── platformio.ini
├── edge_ai/                # Pipeline de entrenamiento TinyML
│   ├── train_agri_model.py
│   └── requirements.txt
├── backend/                # API Gateway con FastAPI
│   └── api.py
└── docs/                   # Documentación de arquitectura y BOM
    ├── architecture.md
    └── hardware_bom.md
python3 -m venv venv
source venv/bin/activate
pip install -r edge_ai/requirements.txt
python3 edge_ai/train_agri_model.py
pip install fastapi uvicorn
uvicorn backend.api:app --reload
---

#### 9. Licencia MIT (`LICENSE`)

```bash
cat << 'EOF' > LICENSE
MIT License

Copyright (c) 2026 Seykarim R. Mestre Zalabata

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
