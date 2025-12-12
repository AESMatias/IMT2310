# Datos entregados en el enunciad, N es el producto de dos primos grandes p y q (el producto es impar),
# mientras que E es la public key, y ciphertext es el mensaje cifrado, queremos "crackear" el RSA mediante
# descomponer N en p y q, para encontrar la private key d necesaria para descifrar el mensaje.
# La idea es, primero factorizar N, luego calcular phi(N) = (p-1)(q-1), 
# luego hallar la private key como el inverso modular de E mod phi(N),
# y finalmente descifrar el mensaje con m = ciphertext^(private_key) mod N.
N = 3000001358000041547
E = 10025
ciphertext = 2952104069193032626

# Máximo común divisor mediante el algoritmo de Euclides
def mcd(p, q):
    ''' Esta función calcula el máximo común divisor de p y q, aquí
    la función no maneja errores cuando q<=0 o p<0, porque asumimos que 
    los datos de entrada son correctos.'''
    while q:
        p, q = q, p % q
    return p

def factorizar_semiprimo(number):
    '''
    Aquí buscamos descomponer number en dos factores primos p y q, tal que number = p * q,
    para esto probamos dividiendo number por todos los números impares a partir de 3,
    hasta que encontremos un divisor exacto.
    '''
    # No es necesario buscar 2 porque N=number es un número impar, ya que es producto
    # de dos primos grandes impares.
    a = 3
    while True:
        if number % a == 0:
            p = a
            q = number // p
            return p, q
        a += 2

    # Si llega aquí, no se encontró el factor, N era primo, lo que es imposible en RSA,
    # porque N es producto de dos primos grandes impares, por lo que esto no debería suceder.
    return 1, n

# Obtenemos el módulo inverso: halla d tal que (a * d) % m == 1
def get_modular_inverse(a, m):
    '''
    Esta función halla los coeficientes x,y tales que a*x + m*y = mcd(a,m), donde
    x es el inverso modular de (a módulo m) si y sólo si (<=>) mcd(a,m)=1, y si
    a y m no son coprimos, la función raisea un error.
    '''

    if mcd(a, m) != 1: 
        raise ValueError("No existe inverso modular para estos valores, ya que a y m no son coprimos!")

    # Aquí, s_prev es el coeficiente para a, y t_prev es el coeficiente para m,
    # que inicializamos en 1 y 0 respectivamente, porque inicialmente tenemos a*1 + m*0 = a,
    # luego iteramos hasta que el residuo actual llegue a cero, y en cada iteración
    # hacemos que el residuo actual sea el residuo anterior menos el cociente por el residuo actual,
    # y actualizamos los coeficientes s y t de la misma manera.
    s_prev, s_curr = 1, 0
    t_prev, t_curr = 0, 1
    residuo_prev, residuo_curr = a, m

    while residuo_curr != 0: # Mientras el residuo actual no llegue a cero, iteramos
        quotient = residuo_prev // residuo_curr
        residuo_prev, residuo_curr = residuo_curr, residuo_prev - quotient * residuo_curr
        s_prev, s_curr = s_curr, s_prev - quotient * s_curr
        t_prev, t_curr = t_curr, t_prev - quotient * t_curr

    modular_inverse_result = s_prev % m
    return modular_inverse_result

def crackRSA(E, N, ciphertext):
    '''
    Primero que nada, debemos factorizar N para obtener los primos p y q, luego calculamos la función phi de Euler, que es
    phi(N) = (p-1)(q-1), luego debemos encontrar la private_key, que se obtiene con la operación
    módulo inverso de E mod phi(N), usando el algoritmo extendido para calcular el máximo común divisor.
    Finalmente, desciframos el mensaje con el exponente modular: M = ciphertext^private_key mod N'''

    p, q = factorizar_semiprimo(N) # p y q son los factores primos de N

    phi = (p - 1) * (q - 1) # Función Phi de Euler para N = p*q

    private_key = get_modular_inverse(E, phi) # d es la private key, obtenido con el inverso modular de E mod phi(N)

    message = pow(ciphertext, private_key, N) # Desciframos el mensaje con la private key
    return message

print('message = ', crackRSA(E, N, ciphertext))