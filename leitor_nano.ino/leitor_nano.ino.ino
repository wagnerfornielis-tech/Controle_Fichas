#include <WiFi.h>
#include <HTTPClient.h>

// Configurações Wi-Fi
const char* ssid = "Pithucos 2G";
const char* password = "Mimi@2018";
const char* serverUrl = "http://192.168.1.104:5000/api/ficha"; // Substitua pelo IP do seu PC

// Pino do aceitador de fichas
const int pinFicha = 23;

// Variáveis para debounce e contagem
bool ultimoEstado = HIGH;        // Estado anterior do pino
bool ficha_detectada = false;    
unsigned long ultimaInterrupcao = 0;
const unsigned long debounceDelay = 150; // 150ms debounce

void setup() {
  Serial.begin(115200);

  // Conectar Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("IP do ESP: ");
  Serial.println(WiFi.localIP());

  // Configurar pino do aceitador
  pinMode(pinFicha, INPUT_PULLUP);
}

void loop() {
  // Leitura do estado atual do pino
  bool estadoAtual = digitalRead(pinFicha);

  // Detecta transição HIGH -> LOW (clique)
  if (ultimoEstado == HIGH && estadoAtual == LOW) {
    unsigned long agora = millis();
    if (agora - ultimaInterrupcao > debounceDelay) {
      ficha_detectada = true;
      ultimaInterrupcao = agora;
    }
  }

  ultimoEstado = estadoAtual;

  // Processa ficha detectada
  if (ficha_detectada) {
    ficha_detectada = false;

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json");

      String json = "{\"fichas\":1}";
      int httpResponseCode = http.POST(json);

      if (httpResponseCode > 0) {
        Serial.printf("Ficha enviada! Resposta: %d\n", httpResponseCode);
      } else {
        Serial.printf("Erro ao enviar: %s\n", http.errorToString(httpResponseCode).c_str());
      }

      http.end();
    } else {
      Serial.println("Wi-Fi desconectado. Tentando reconectar...");
      WiFi.reconnect();
    }
  }

  delay(10); // loop rápido suficiente para processar cliques
}
