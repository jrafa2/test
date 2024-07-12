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
ser = serial.Serial('COM3', 115200)
#ser = serial.Serial('/dev/ttyUSB0')  # linux

ser.open()
instr = rm.open_resource('USB0::0x0400::0x09C4::DG1D181702050::INSTR')

writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

################################
# Configuration
################################
instr.write('*IDN?')
instr_res = instr.read()
print(f'Waveform source: {instr_res}')

instr.write('SOUR:FUNC SIN')   # set DC
instr.write('SOUR:VOLT 2.5')  # initial voltage
instr.write('SOUR:VOLT:OFFS 2')  # initial offset
instr.write('SOUR:FREQ 100')
instr.write('OUTP ON')  # enable output

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
    instr_res = instr.write('SOUR:FREQ ' + str((float(f))))
    print(f'Set frequency: {f}')
    
    time.sleep(2) # Sleep for 2 seconds
    
    # Read ADC value
    for i in iterations:
        ser.write(bytes('r', 'utf-8'))
        adc_val = int(ser.readline())
        adc_val_volt = adc_val * (5.0 / 1023.0)
        print(f'Read ADC: {adc_val} ({adc_val_volt})')
    
        # Write
        writer.writerow([current_timestamp, i, f, adc_val])
    
################################
# Close resources
################################
instr.write('OUTP OFF')  # disable output

instr.close()
ser.close()
f.close()
