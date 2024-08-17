#serial control of relay board
#UD74B08 8ch IO Digital USB COM Serial Port UART Relay Module
import serial #python.exe -m pip install pyserial
import sys
import time


def calculate_checksum(command_bytes):
    return sum(command_bytes) % 256

def create_command(relay, action):
    header = [0x55, 0x56]
    zeros = [0x00, 0x00, 0x00]
    command = header + zeros + [relay, action]
    checksum = calculate_checksum(command)
    command.append(checksum)  
    return bytearray(command)

def send_command(port, relay, action):
    try:
        with serial.Serial(
            port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        ) as ser:
            command = create_command(relay, action)
            ser.write(command)
            ser.flush()  # Ensure all data is sent
            time.sleep(0.1)  # Add a small delay            
            print(f"Sent command: {' '.join(format(x, '02X') for x in command)}")
    except serial.SerialException as e:
        print(f"Error: {e}")
        sys.exit(1)
       
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python relay_control.py <COM_PORT> <RELAY_NUMBER> <ACTION>")
        print("RELAY_NUMBER: 1-8")
        print("ACTION: 1=ON, 2=OFF, 3=TOGGLE, 4=MOMENTARY ON")
        sys.exit(1)

    port = sys.argv[1]
    relay = int(sys.argv[2])
    action = int(sys.argv[3])

    if relay < 1 or relay > 8:
        print("Error: Relay number must be between 1 and 8.")
        sys.exit(1)

    if action < 1 or action > 4:
        print("Error: Action must be 1 (ON), 2 (OFF), 3 (TOGGLE), or 4 (MOMENTARY ON).")
        sys.exit(1)

    send_command(port, relay, action)