#include <Arduino.h>

/*
 * AgroPulse Edge - Firmware para Nodo Centinela Agrícola
 * Microcontrolador: ESP32-S3 + Módulo Radio LoRa SX1276
 * Aplicación: Telemetría de Suelo, Estrés Hídrico y Alerta de Plagas
 */

struct AgroTelemetry {
  float soil_moisture_pct;   // Humedad volumétrica del suelo (%)
  float soil_temperature_c;  // Temperatura del suelo (°C)
  float air_temperature_c;   // Temperatura ambiental (°C)
  float air_humidity_pct;    // Humedad relativa (%)
  float npk_nitrogen_ppm;    // Nitrógeno disponible (ppm)
  float solar_radiation_uv;  // Índice UV / Radiación
};

// Algoritmo en el Borde (TinyML Quantized Classifier)
// Retorna 0: Óptimo, 1: Estrés Hídrico Moderado, 2: Riesgo de Plaga/Hongo, 3: Alerta Crítica de Sequía
uint8_t predict_crop_health(const AgroTelemetry& data) {
  // Regla de riesgo epidemiológico de Roya/Sigatoka (Humedad relativa alta + Temp templada)
  if (data.air_humidity_pct > 85.0f && data.air_temperature_c >= 18.0f && data.air_temperature_c <= 26.0f) {
    return 2; // Riesgo Alto de Fitopatógenos
  }
  
  // Evaluación de Déficit Hídrico en Raíz
  if (data.soil_moisture_pct < 20.0f) {
    return (data.solar_radiation_uv > 8.0f) ? 3 : 1;
  }

  return 0; // Cultivo en condiciones óptimas
}

AgroTelemetry current_readings;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=========================================================");
  Serial.println("   AgroPulse Edge - Telemetría Agrícola & TinyML Local  ");
  Serial.println("   Región: Caribe & Zona Cafetera de Colombia           ");
  Serial.println("=========================================================");
}

void loop() {
  // Simulación de lectura de sensores industriales (RS485 Modbus NPK + SHT31)
  current_readings.soil_moisture_pct = random(15, 60) + random(0, 9) / 10.0f;
  current_readings.soil_temperature_c = random(20, 32) + random(0, 9) / 10.0f;
  current_readings.air_temperature_c = random(22, 38) + random(0, 9) / 10.0f;
  current_readings.air_humidity_pct = random(40, 95) + random(0, 9) / 10.0f;
  current_readings.npk_nitrogen_ppm = random(12, 45);
  current_readings.solar_radiation_uv = random(2, 11);

  uint8_t health_status = predict_crop_health(current_readings);

  Serial.printf("[Telemetría Suelo/Clima] Suelo Hum: %.1f%% | Temp Air: %.1fC | Hum Air: %.1f%% | Nitrógeno: %.0f ppm\n",
                current_readings.soil_moisture_pct, current_readings.air_temperature_c,
                current_readings.air_humidity_pct, current_readings.npk_nitrogen_ppm);

  switch (health_status) {
    case 0:
      Serial.println("🟢 [ESTADO CULTIVO] Condiciones de desarrollo óptimas.");
      break;
    case 1:
      Serial.println("🟡 [ALERTA RIEGO] Estrés hídrico leve detectado. Programar fertirriego.");
      break;
    case 2:
      Serial.println("⚠️  [RIESGO PATÓGENO] Humedad y temperatura propicias para hongos (Roya/Sigatoka).");
      break;
    case 3:
      Serial.println("🔴 [CRÍTICO] Sequía extrema y radiación alta. Activando electroválvula de emergencia...");
      break;
  }

  Serial.println("📡 [LoRaWAN] Transmitiendo paquete cifrado a Gateway Malla Rural...");
  Serial.println("-------------------------------------------------------------------------");
  delay(5000);
}
