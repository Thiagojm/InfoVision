import secrets
import time


bit_size = 8192

t0 = time.time()
bits = secrets.randbits(bit_size)
print(bits)
bin_ascii = bin(bits)[2:].zfill(bit_size)
print("Binary String: ", bin_ascii)
print("Binary lenght: ", len(bin_ascii))
num_ones_array = bin_ascii.count('1')
print("Number of 'ones': ", num_ones_array)
print(time.time() - t0)

##############################

t0 = time.time()
x_bits = ""

for i in range(bit_size):
    i = secrets.randbelow(2)
    x_bits += str(i)

print("Binary String: ", x_bits)
print("Binary lenght: ", len(x_bits))
print("Number of 'ones': ", x_bits.count('1'))
print(time.time() - t0)

