import serial
import serial.tools.list_ports
import time

def encontrar_porta():
    """Procura automaticamente a porta do ESP32"""
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        # alguns ESP32 aparecem como 'USB-SERIAL', 'Silicon Labs', 'CH340' etc.
        if "USB" in porta.description or "Silicon" in porta.description or "CH340" in porta.description:
            print(f"ESP32 encontrado em: {porta.device}")
            return porta.device
    # se não achou, pede para o usuário
    print("Nenhuma porta de ESP32 detectada. Use COM manualmente.")
    return None

def modo_serial():
    porta = encontrar_porta()
    if not porta:
        return
    
    try:
        ser = serial.Serial(porta, 115200, timeout=1)
        print(f"Conectado à porta {porta}. Aguardando dados...\n")

        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode(errors="ignore").strip()
                if linha:
                    print("Recebido:", linha)
            time.sleep(0.1)
    except Exception as e:
        print("Erro ao abrir porta:", e)

if __name__ == "__main__":
    modo_serial()
