import pyvisa
import serial
import numpy
import time
import calendar
import csv

csvfile = 'measures_f_' + str(time.time()) + '.csv'
num_meas_per_freq = 100

################################
# Open resources
################################
rm = pyvisa.ResourceManager()
ser = serial.Serial('COM1', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
#ser = serial.Serial('/dev/ttyUSB0')  # linux

ser.open()
instr = rm.open_resource('GPIB::10::INSTR')

writer = csv.writer(csvfile, delimiter='; ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

################################
# Configuration
################################
instr_res = instr.query('*IDN?')
print(f'Waveform source: {instr_res}')

instr.query('SOUR:FUNC SIN')   # set DC
instr.query('SOUR:VOLT 2.5')  # initial voltage
instr.query('SOUR:VOLT:OFFS 2')  # initial offset
instr.query('OUTP ON')  # enable output

writer.writerow(['Timestamp', 'Iteration', 'f', 'ADCval'])

utc_timestamp = calendar.timegm(utc_time_tuple)
print("UTC Timestamp: ", utc_timestamp)

################################
# Iterate
################################
freqs = np.logspace(0, 10e6, 10)
iterations = range(1, num_meas_per_freq)
for f in freqs:
    current_timestamp = time.time()

    # Set a voltage
    instr_res = instr.query('SOUR:FREQ ' + str((float(f))))
    print(f'Set frequency: {f}')
    
    time.sleep(2) # Sleep for 2 seconds
    
    # Read ADC value
    for i in iterations:
        adc_val = int.from_bytes(ser.read(4), byteorder='big')
        adc_val_volt = adc_val * (5.0 / 1023.0)
        print(f'Read ADC: {adc_val} ({adc_val_volt})')
    
        # Write
        writer.writerow([current_timestamp, i, f, adc_val])
    
instr.close()
ser.close()
writer.close()
csv.close()