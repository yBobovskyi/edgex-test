from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep

server = ModbusServer(host = 'edgex-switch', port = 1502, no_block=True)

try:
    server.start()
    print("Server started")
    DataBank.set_bits(0, [True])
    while True:
        state = DataBank.get_bits(0)
        f = open('state', 'w')
        if state[0]:
            f.write("ON")
        else:
            f.write("OFF")
        f.close()
        sleep(3)
except Exception as e:
    print(str(e))
    server.stop()
    print("Server shut down")
