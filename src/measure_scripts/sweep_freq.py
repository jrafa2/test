import pyvisa
import serial
import time
import calendar
import datetime
import csv
import numpy as np

csvfile = 'measures_f_' + str(time.time()) + '.csv'
num_meas_per_freq = 100

################################
# Open resources
################################
rm = pyvisa.ResourceManager()
ser = serial.Serial('COM3', 115200)
#ser = serial.Serial('/dev/ttyUSB0')  # linux

if(ser.isOpen() == False):
    ser.open()
instr = rm.open_resource('USB0::0x0400::0x09C4::DG1D181702050::INSTR')

fil = open(csvfile, mode='w')

writer = csv.writer(fil, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

################################
# Configuration
################################
instr.write('*IDN?')
time.sleep(1)   #wait for the instrument to answer
instr_res = instr.read()
print(f'Waveform source: {instr_res}')

instr.write('APPL:SIN 100,2.5,2.5')   # set sin function
instr.write('OUTP ON')  # enable output

writer.writerow(['Timestamp', 'Iteration', 'f', 'ADCval'])

utc_timestamp = datetime.datetime.now()
print("UTC Timestamp: ", utc_timestamp)

################################
# Iterate
################################
freqs = np.logspace(1, 6, num=50)
iterations = range(1, num_meas_per_freq)
max_val = 0;
for f in freqs:
    current_timestamp = time.time()

    # Set a voltage
    instr_res = instr.write('APPL:SIN ' + str((float(f))) + ',2.5,2.5')
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
        
        # Get the peak value
        if(adc_val > max_val):
            max_val = adc_val
            
    print(f'Max value: {max_val}')   #BW is when amplitud is 1/2
    
################################
# Close resources
################################
instr.write('OUTP OFF')  # disable output

instr.close()
ser.close()
fil.close()
