


#    
#
def bin16Tofloat(b):
    S = (b&0x8000)>>(15)
    E = (b&0x7C00)>>(10)
    M = (b&0x3ff)
    print("b:", hex(b))
    print(f"S: {S}, E: {E}, M: {M}")
#
    if E == 0x0:
        f = (-1)**S*2**(1-15)*(M/2**10)
    else:
        f = (-1)**S*2**(E-15)*(1+M/2**10)
    print("f: ", f)
    return f


import math

def floatTobin16(num):
    # 1. Casos Especiales (Ceros)
    if num == 0.0:
        # math.copysign verifica si es -0.0 o +0.0
        return "0x8000" if math.copysign(1.0, num) < 0 else "0x0000"
#
    # 2. Determinar Signo
    signo = 1 if num < 0 else 0
    num = abs(num)
#
    # 3. Calcular Exponente Real
    exp_real = math.floor(math.log2(num))
#    
    # 4. Calcular Exponente Sesgado (Bias = 15)
    exp_sesgado = exp_real + 15
#
    # 5. Lógica de Mantisa y límites
    if exp_sesgado >= 31:
        # Desbordamiento -> Infinito
        exp_sesgado = 31
        mantisa = 0
    elif exp_sesgado <= 0:
        # Número Subnormal (demasiado pequeño, exp_sesgado es 0)
        exp_sesgado = 0
        # En subnormales, el exponente implícito es -14
        fraccion = num / (2 ** -14)
        mantisa = int(round(fraccion * (2 ** 10)))
    else:
        # Número Normalizado
        fraccion = (num / (2 ** exp_real)) - 1.0
        mantisa = int(round(fraccion * (2 ** 10)))
#        
        # Corrección: si el redondeo desborda los 10 bits (ej. 1024)
        if mantisa == (2**10):
            mantisa = 0
            exp_sesgado += 1
#
    # 6. Ensamblar los bits usando desplazamientos lógicos (Shift OR)
    bits_16 = (signo << 15) | (exp_sesgado << 10) | mantisa
#
    # 7. Formatear como Hexadecimal de 4 dígitos
    #return f"0x{bits_16:04X}"
    #
    return hex(bits_16)



# para 32 bits:
#    falta descripcion
#    sin construir

def bin32Tofloat(b):
    S = (b&0x80000000)>>(31)
    E = (b&0x7F800000)>>(23)
    M = (b&0x007fffff)
    print("b:", hex(b))
    print(f"S: {S}, E: {E}, M: {M}")
#
    if E == 0x0:
        f = (-1)**S*2**(1-127)*(M/2**23)
    else:
        f = (-1)**S*2**(E-127)*(1+M/2**23)
    print("f: ", f)
    return f


import math

def floatTobin32(num):
    # 1. Casos Especiales (Ceros)
    if num == 0.0:
        # math.copysign verifica si es -0.0 o +0.0
        return "0x80000000" if math.copysign(1.0, num) < 0 else "0x00000000"

    # 2. Determinar Signo
    signo = 1 if num < 0 else 0
    num = abs(num)

    # 3. Calcular Exponente Real
    exp_real = math.floor(math.log2(num))
    
    # 4. Calcular Exponente Sesgado (Bias = 127 para 32 bits)
    exp_sesgado = exp_real + 127

    # 5. Lógica de Mantisa y límites
    if exp_sesgado >= 255:
        # Desbordamiento -> Infinito
        exp_sesgado = 255
        mantisa = 0
    elif exp_sesgado <= 0:
        # Número Subnormal (demasiado pequeño, exp_sesgado es 0)
        exp_sesgado = 0
        # En subnormales de 32 bits, el exponente implícito es -126
        fraccion = num / (2 ** -126)
        mantisa = int(round(fraccion * (2 ** 23)))
    else:
        # Número Normalizado
        fraccion = (num / (2 ** exp_real)) - 1.0
        mantisa = int(round(fraccion * (2 ** 23)))
        
        # Corrección: si el redondeo desborda los 23 bits (2^23)
        if mantisa == (2 ** 23):
            mantisa = 0
            exp_sesgado += 1
            if exp_sesgado >= 255:
                exp_sesgado = 255

    # 6. Ensamblar los bits usando desplazamientos lógicos (Shift OR)
    # Signo en bit 31, Exponente en bits 23-30, Mantisa en bits 0-22
    bits_32 = (signo << 31) | (exp_sesgado << 23) | mantisa

    # 7. Formatear como Hexadecimal de 8 dígitos
    #return f"0x{bits_32:08X}"
    #
    return hex(bits_32)





# --- Ejemplos de uso ---
print(f"32.5   -> {floatTobin16(32.5)}")   # Salida: 0x5010
print(f"4.332  -> {floatTobin16(4.332)}")  # Salida: 0x4455
print(f"-0.307 -> {floatTobin16(-0.307)}") # Salida: 0xB4E9

print("La implementacion falla para casos extremos!")

N = -35000
div = -0.307

print(f"\n\ndivision natural: {N}/{div} == 114006.51\n\n")
b = floatTobin16(114006.51) #'0x7c00'
print(f"resultado hex: {b}")

#divi_impl(N, div) # 0x7ef6
n1 = floatTobin16(-35000)
n2 = floatTobin16(-0.307)
print(f"\n\ndivi_impl({N}: {n1}, {div}: {n2}) == 0x7ef6\n\n")
f = bin16Tofloat(0x7ef6) # 114048.0

print(bin16Tofloat)
print(floatTobin16)