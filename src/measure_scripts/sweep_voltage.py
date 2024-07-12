import pyvisa
import serial
import time
import calendar
import csv

csvfile = 'measures_v_' + str(time.time()) + '.csv'
num_meas_per_voltage = 10

################################
# Open resources
################################
rm = pyvisa.ResourceManager()
ser = serial.Serial('COM3', 115200)
#ser = serial.Serial('/dev/ttyUSB0')  # linux

ser.open()
instr = rm.open_resource('USB0::0x0400::0x09C4::DG1D181702050::INSTR')

f = open(csvfile, mode='w')

writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

################################
# Configuration
################################
instr.write('*IDN?')
instr_res = instr.read()
print(f'Waveform source: {instr_res}')

instr.write('SOUR:FUNC DC')   # set DC
instr.write('APPL:DC DEF,DEF,0')  # initial voltage
instr.write('OUTP ON')  # enable output

writer.writerow(['Timestamp', 'Iteration', 'V', 'ADCval'])

utc_timestamp = calendar.timegm(utc_time_tuple)
print("UTC Timestamp: ", utc_timestamp)

################################
# Iterate
################################
voltages = range(0, 5, 0.001)  #less than LSB to cover all codes
iterations = range(1, num_meas_per_voltage)
for v in voltages:
    current_timestamp = time.time()

    # Set a voltage
    instr.write('APPL:DC DEF,DEF,' + str((float(v))))
    print(f'Set voltage: {v}')
    
    time.sleep(2) # Sleep for 2 seconds

    # Read ADC value
    for i in iterations:
        ser.write(bytes('r', 'utf-8'))
        adc_val = int(ser.readline())
        adc_val_volt = adc_val * (5.0 / 1023.0)
        print(f'Read ADC: {adc_val} ({adc_val_volt})')
    
        # Write
        writer.writerow([current_timestamp, i, v, adc_val])

################################
# Close resources
################################
instr.write('OUTP OFF')  # disable output

instr.close()
ser.close()
f.close()
