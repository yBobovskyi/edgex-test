import glob

temp_path = '/sys/devices/platform/coretemp.0/hwmon/hwmon5/temp*_input'

def get_cpu_temps():
    file_list = glob.glob(temp_path)
    cpu_temps = []
    for file in file_list:
        with open(file, 'r') as temp_file:
            cpu_temps.append(int(temp_file.readline()) / 1000)
    return cpu_temps