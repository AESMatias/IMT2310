import random

class CodeSpec:
    def __init__(self,messageBits,parityBits,paritySets):
        self.messageBits = messageBits # length of the original message
        self.parityBits = parityBits # number of parity sets/bits
        self.paritySets = paritySets # an array of parity sets

    def correctErasures(self, code):
        # Almacenamos una copia del código en memoria por valor, no por referencia, así los test no se ven afectados:
        list_of_code = list(code)

        # Hacemos un bucle while hasta que en una iteración no se pueda reconstruir nada del código original.
        code_has_been_changed = True # Debe ser True para iniciar el bucle, si no hay cambios se sale del bucle

        while code_has_been_changed:
            code_has_been_changed = False  # Marcador para saber si en esta vuelta reconstruimos algo

            for paritySet in self.paritySets:
                # En el parity set buscamos posiciones de bits desconocidas con signo ?
                unknown_positions = []
                
                for idx in paritySet:
                    if list_of_code[idx] == '?':
                        unknown_positions.append(idx) # Si encontramos una posición de un bit desconocido, la almacenamos
                        # print(f"- Unknown position in MESSAGEEEEE {list_of_code} found in the index {idx} -")

                unknow_bits_quantity = len(unknown_positions)
                        

                if unknow_bits_quantity == 1: # Únicamente podemos reconstruir el código si hay exactamente una incógnita en este parity set
                    current_missing_idx = unknown_positions[0]

                    parity_sum = 0
                    # Ahora, hacemos un bucle y vamos sumando la paridad de cada bit conocido en el parity set,
                    # para obtener la paridad total del set (la suma debe ser par, es decir, 0 módulo 2).
                    for idx in paritySet:
                        if list_of_code[idx] != '?':  # Sólo sumamos los bits ya reconstruidos o recibidos
                            parity_sum = (parity_sum + int(list_of_code[idx])) % 2 # Sumamos módulo 2, para obtener paridad par.

                    list_of_code[current_missing_idx] = parity_sum # Cambiamos el valor de paridad al bit que falta
                    code_has_been_changed = True  # Indicamos que en esta iteración hubo un cambio, para volver a iterar!
                    
        # Esto retornará una list comprehension que convierte los bits '0' y '1' a números enteros, y deja los signos ? en string:
        return [int(n) if n in ('0', '1') else n for n in list_of_code] # Si no se pudo reconstruir todo, quedarán signos ? en el código


class GenTests:
    def __init__(self,messageBits,parityBits,parityLength,message):
        self.messageBits = messageBits # length of the original message
        self.parityBits = parityBits # number of parity sets/bits
        self.parityLength = parityLength # size of each parity set
        self.paritySets = self.generateParitySets() # an array of parity sets
        self.code = self.generate_code(message)

    def generateParitySets(self):

        paritySets = []

        for i in range(self.parityBits): # generate the i-th parity set
            paritySet = set()
            paritySet.add(self.messageBits + i)
            j = 1
            while j < self.parityLength: # each set has parityLength positions
                message_pos = random.randint(0, self.messageBits - 1)
                if (message_pos not in paritySet):
                    j = j + 1
                    paritySet.add(message_pos)

            paritySets.append(paritySet)    

        return paritySets

    def generate_code(self,message):
        code = [0]*(self.messageBits + self.parityBits)
        for i in range(len(message)):
            code[i] = message[i]
        assert (len(message) == self.messageBits), "Length must match"
        i = 0
        for paritySet in self.paritySets:
            sum = 0
            for index in paritySet:
                if (index < self.messageBits):
                    sum = sum + message[index]
            code[self.messageBits+i] = sum % 2
            i = i +1
        return code


def run_test(name, message_bits, parity_bits, parity_length, parity_sets, code, transmitted):
    print(f"Test - {name}")

    test = GenTests(message_bits, parity_bits, parity_length, code[:message_bits])
    test.paritySets = parity_sets
    test.code = list(code)

    print('Parity sets: ',test.paritySets)
    print('Code: ', test.code)

    code_spec = CodeSpec(message_bits, parity_bits, test.paritySets)
    recovered = code_spec.correctErasures(list(transmitted))
    print('Recovered: ', recovered)
    print()


def run_all_tests():
    demo = GenTests(8, 4, 4, [1, 1, 1, 1, 0, 0, 1, 1])
    demo_transmission = list(demo.code)
    demo_transmission[3] = '?'
    demo_transmission[5] = '?'
    run_test("Demo", 8, 4, 4, demo.paritySets, demo.code, demo_transmission)

    run_test(
        "Test1",
        8,
        4,
        4,
        [{8, 4, 5, 6}, {0, 9, 3, 4}, {2, 10, 3, 4}, {1, 11, 6, 7}],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, '?', 0, '?', 1, 1, 1, 0, 0, 1],
    )

    run_test(
        "Test2",
        8,
        4,
        4,
        [{8, 4, 5, 7}, {9, 2, 3, 5}, {1, 10, 5, 7}, {1, 2, 11, 7}],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, '?', 0, '?', 1, 1, 1, 0, 0, 1],
    )

    run_test(
        "Test3",
        8,
        4,
        4,
        [{8, 0, 6, 7}, {9, 3, 6, 7}, {1, 10, 6, 7}, {0, 11, 4, 7}],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, '?', 0, '?', 1, 1, 1, 1, 1, 0],
    )

    run_test(
        "Test4",
        8,
        4,
        4,
        [{8, 1, 6, 7}, {9, 4, 1, 6}, {1, 10, 6, 7}, {0, 1, 2, 11}],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, '?', 0, 0, 1, 1, 1, 0, 1, '?'],
    )

    run_test(
        "Test5",
        8,
        4,
        4,
        [{8, 1, 4, 7}, {9, 3, 5, 6}, {1, 10, 2, 7}, {2, 11, 4, 6}],
        [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        [1, 1, 1, '?', 0, '?', 1, 1, 0, 0, 1, 0],
    )


if __name__ == "__main__":
    run_all_tests()



###########
###Test1###
###########

#paritySets = [{8, 4, 5, 6}, {0, 9, 3, 4}, {2, 10, 3, 4}, {1, 11, 6, 7}]
#code = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1]
#transmittedCode = [1, 1, 1, '?', 0, '?', 1, 1, 1, 0, 0, 1]
# correct all


###########
###Test2###
###########

#paritySets = [{8, 4, 5, 7}, {9, 2, 3, 5}, {1, 10, 5, 7}, {1, 2, 11, 7}]
#code = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1]
#transmittedCode = [1, 1, 1, '?', 0, '?', 1, 1, 1, 0, 0, 1]
# needs to correct 5 first, three next
#output = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1]


###########
###Test3###
###########

#paritySets = [{8, 0, 6, 7}, {9, 3, 6, 7}, {1, 10, 6, 7}, {0, 11, 4, 7}]
#code = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0]
#transmittedCode = [1, 1, 1, '?', 0, '?', 1, 1, 1, 1, 1, 0]
#output = [1, 1, 1, 1, 0, '?', 1, 1, 1, 1, 1, 0]
# can only reconstruct 3


###########
###Test4###
###########

#paritySets = [{8, 1, 6, 7}, {9, 4, 1, 6}, {1, 10, 6, 7}, {0, 1, 2, 11}]
#code = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]
#transmittedCode = [1, 1, 1, '?', 0, 0, 1, 1, 1, 0, 1, '?']
# output = [1, 1, 1, '?', 0, 0, 1, 1, 1, 0, 1, 1]
# we can only reconstruct parity bit 11, but not position 3!


###########
###Test5###
###########

#paritySets = [{8, 1, 4, 7}, {9, 3, 5, 6}, {1, 10, 2, 7}, {2, 11, 4, 6}]
#code = [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
#transmittedCode = [1, 1, 1, '?', 0, '?', 1, 1, 0, 0, 1, 0]
# output = [1, 1, 1, '?', 0, '?', 1, 1, 0, 0, 1, 0]