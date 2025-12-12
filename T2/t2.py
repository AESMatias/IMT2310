from itertools import combinations

class Grupo:
	def __init__(self, num, cayley):
		self.n = num
		self.cayley = cayley
		self.neutro = self.elemento_neutro()
		self.es_grupo = self.es_grupo()
		self.abeliano = self.es_abeliano()


	def is_closed(self):
		for row, col in enumerate(self.cayley):
			for element in col:
				# Cada elemento es como mínimo 0, y como máximo n-1 (que es self.n -1)
				if element < 0 or element > (self.n-1):
					return False
		return True


	def is_associative(self) -> bool:
		# Comprobar la asociatividad: (a * b) * c == a * (b * c)
		for a in range(self.n):
			for b in range (self.n):
				for c in range(self.n):
					# Primero calculamos (a * b) * c
					ab_left = self.cayley[a][b] # (a * b)
					abc_left = self.cayley[ab_left][c] # (a * b) * c
					# Luego calculamos a * (b * c)
					bc_right = self.cayley[b][c] # (b * c)
					abc_right = self.cayley[a][bc_right] # a * (b * c)
					# Comparamos los dos resultados
					if abc_left != abc_right:
						return False
		return True

	def has_identity_element(self) -> bool:
		identity = self.neutro
		if identity is not None:
			return True
		return False

 
	# busca el elemento neutro; si hay mas que uno, o si no hay uno tira una exepcion
	def elemento_neutro(self) -> int | None:
		# El elemento neutro es tal que, para todo a en G, e * a = a * e = a. Es decir, deja cada elemento tal cual,
		# ya sea si se aplica la operación a la izquierda o a la derecha de dicho elemento.

		possible_identities = [] # Si existe más de un supuesto elemento neutro, no es grupo!

		for e in range(self.n):
			is_identity = True # Asumimos que e es el elemento neutro, si algún caso falla, no lo es.
			for a in range(self.n):
				if self.cayley[e][a] != a or self.cayley[a][e] != a:
					is_identity = False
					break # No es necesario seguir comprobando para a.
			if is_identity:
				possible_identities.append(e)
		if len(possible_identities) == 1:
				return possible_identities[0]
		return None


	def has_inverse_elements(self) -> bool:
		identity_element = self.neutro
		if identity_element is None:
			return False # Si no existe el elemento neutro, no puede existir inversa para los elementos del grupo.

		for a in range(self.n):
			has_inverse = False # Ponemos False a cada nuevo elemento a que consideremos, si lo encontramos cambia a True.
			for b in range(self.n):
				if self.cayley[a][b] == identity_element and self.cayley[b][a] == identity_element:
					has_inverse = True # Encontramos el inverso para ese elemento a en particular.
					break # No es necesario seguir buscando inverso para a.
			if not has_inverse:
				return False
		return True # Encontramos inversa para todos los elementos a en el grupo!


	# Tetorna false si la tabla cayley no define a un grupo, sino true
	def es_grupo(self) -> bool:
		'''Para que una tabla de Cayley defina un grupo, se deben cumplir 4 propiedades de grupo:
		1 - Clausura: Para todo a, b en G, el resultado de la operacion a * b tambien esta en G
		2 - Asociatividad: Para todo a, b, c en G, (a * b) * c = a * (b * c)
		3 - Elemento neutro: Existe un elemento e en G tal que para todo a en G, e * a = a * e = a
		4 - Elemento inverso: Para cada a en G, existe un elemento b en G tal que a * b = b * a = e'''
  
		if not self.is_closed(): # Propiedad 1: Clausura sobre el conjunto.
			print("La tabla de Cayley NO DEFINE UN GRUPO, falla la propiedad de Clausura")
			return False
		if not self.is_associative(): # Propiedad 2: Asociatividad
			print("La tabla de Cayley NO DEFINE UN GRUPO, falla la propiedad de Asociatividad")
			return False
		if not self.has_identity_element(): # Propiedad 3: Elemento neutro
			print("La tabla de Cayley NO DEFINE UN GRUPO, falla la propiedad del Elemento neutro")
			return False
		if not self.has_inverse_elements(): # Propiedad 4: Elemento inverso
			print("La tabla de Cayley NO DEFINE UN GRUPO, falla la propiedad del Elemento inverso")
			return False
		print("La tabla de Cayley DEFINE UN GRUPO, cumple las 4 propiedades.")
		return True


	# valor booleano que dice si el grupo es abeliano
	def es_abeliano(self):
		'''Para comprobar que un grupo es abeliano, debemos verificar que para todo a, b en G, se cumple que a * b = b * a,
		pero también se puede ver como que la tabla de Cayley es simétrica respecto a la diagonal.'''
  
		if not self.es_grupo:
			print("No tiene sentido preguntar si es abeliano, porque NO ES UN GRUPO")
			return False

		for a in range(self.n):
			for b in range(self.n):
				if self.cayley[a][b] != self.cayley[b][a]:
					# Si operar a con b no es igual que operar b con a, no es abeliano (no es conmutativo para todo a,b in G).
					print("El grupo NO ES ABELIANO")
					return False
		return True


	# Recibe un conjunto de elementos del grupo (dado en la variable elementos), y decide si
	# estos elementos forman un subgrupo de nuestro grupo; se imprime si/no
	def es_subgrupo(self, elementos):
     # Hay un axioma que dice que todo subgrupo contiene el elemento neutro del grupo que lo contiene, así que buscamos
     # si existe ese elemento neutro de G en el supuesto subgrupo H
		has_identity_element = False
  
		for elem in elementos:
			if elem < 0 or elem > (self.n-1):
				print("no") # Se pidió que imprima "no" en el PDF del enunciado.
				return False
		if self.neutro not in elementos:
			print("no") # Se pidió que imprima "no" en el PDF del enunciado.
			return False
		else:
			has_identity_element = True

		for elem in elementos: # Buscamos el inverso de elem en el conjunto de elementos dados
			has_inverse = False
			for candidate in elementos:
				if self.cayley[elem][candidate] == self.neutro == self.cayley[candidate][elem]:
					has_inverse = True
					break
			if has_inverse == False:
				print("no") # Se pidió que imprima "no" en el PDF del enunciado.
				return False

		for elem in elementos: # Ahora comprobamos que es cerrado bajo la operación del grupo:
			for other_elem in elementos: # Ya se recorre arriba, con este segundo bucle contamos todas las combinaciones
				result = self.cayley[elem][other_elem]
				if result not in elementos:
					print("no") # Se pidió que imprima "no" en el PDF del enunciado.
					return False
    
		if not has_identity_element:
			print("no") # Se pidió que imprima "no" en el PDF del enunciado.
			#print("El conjunto dado NO FORMA UN SUBGRUPO (no contiene el elemento neutro)")
			return False
		print("sí") # Se pidió que imprima "sí" en el PDF del enunciado.
		return True

	def es_subgrupo_without_prints(self, elementos): # MISMA FUNCIÓN QUE LA ANTERIOR, PERO SIN PRINTS QUE MOLESTEN
     # Hay un axioma que dice que todo subgrupo contiene el elemento neutro del grupo que lo contiene, así que buscamos
     # si existe ese elemento neutro de G en el supuesto subgrupo H
		has_identity_element = False
  
		for elem in elementos:
			if elem < 0 or elem > (self.n-1):
				return False
		if self.neutro not in elementos:
			return False
		else:
			has_identity_element = True

		for elem in elementos: # Buscamos el inverso de elem en el conjunto de elementos dados
			has_inverse = False
			for candidate in elementos:
				if self.cayley[elem][candidate] == self.neutro == self.cayley[candidate][elem]:
					has_inverse = True
					break
			if has_inverse == False:
				return False

		for elem in elementos: # Ahora comprobamos que es cerrado bajo la operación del grupo:
			for other_elem in elementos: # Ya se recorre arriba, con este segundo bucle contamos todas las combinaciones
				result = self.cayley[elem][other_elem]
				if result not in elementos:
					#print("no") # Se pidió que imprima "no" en el PDF del enunciado.
					return False
    
		if not has_identity_element:
			return False
		return True

	def find_combinations(self, elements_or_groups: list, k: int) -> list:
		'''Esta función genera todas las combinaciones de tamaño size_k de una lista de "elementos", que
        también puede ser una lista de subgrupos, no necesariamente son elementos de un grupo.'''
		return [list(c) for c in combinations(elements_or_groups, k)] # Parseamos porque debe retornarse una lista de listas!


	# Busca si nuestro grupo se puede representar como el producto interno de dos subgrupos
	# En el caso que si, se imprimen los elementos de los dos subgrupos
	# En el caso que no, se imprime un mensaje senallando esto
	def producto_interno(self):

		if not self.es_grupo:
			print("No es un grupo, por lo tanto no se puede buscar el producto interno!")
			return

		elementos_grupo = list(range(self.n)) # Lista con cantidad de elementos desde 0 hasta n-1
		neutro_set = {self.neutro} # Set con el elemento neutro

		'''Primero que nada, buscamos todos los subgrupos del grupo G, la idea es genrar todas las
  		combinaciones posibles entre los elementos del grupo, y para cada combinación, comprobar si es un subgrupo
    	mediante la función es_subgrupo_without_prints().
     	Luego, con la lista de subgrupos encontrados, generamos todos los pares posibles (H, K) y 
      	comprobamos las 3 condiciones del producto interno para cada par. El par que cumpla las tres condiciones, 
        es un par válido para representar G como producto interno de subgrupos H y K.
        Es impotante mencionar que los pares generados (H,K) se obtienen mediante la operación propia del grupo G,
        pero en este caso no está explícita, así que usamos la tabla de Cayley para obtener directamente 
        los resultados de las operaciones entre elementos de H y K.'''
        
		subgrupos_propios = []
		for n in range(2, self.n): # k=tamaño, desde 2 hasta n-1
			# Esto porque los subgrupos propios no pueden ser ni el grupo trivial {e} (tamaño 1),
			# ni el grupo completo G (tamaño n)
			possible_elements_combinations = self.find_combinations(elementos_grupo, n)

			for subset in possible_elements_combinations:
				if self.es_subgrupo_without_prints(subset):
					# Lo guardamos como set para facilitar las operaciones posteriormente, porque un set 
					# no permite repetidos, y además permite operaciones como intersección, unión, etc:
					subgrupos_propios.append(set(subset))

		if not (len(subgrupos_propios) >= 2):
			print("No se puede representar como producto interno porque no hay suficientes subgrupos propios.")
			return

		'''Generamos todos los pares posibles (H, K) de subgrupos propios. Podemos usar la misma función de combinaciones
  		que antes, pero ahora con size_k=2, porque queremos pares de subgrupos (H, K).'''
		lista_de_pares_hk = self.find_combinations(subgrupos_propios, 2)

		'''Ahora, para cada par (H, K) en la lista de pares, probamos las 3 condiciones del producto interno:
  		1 - |H| * |K| = |G|  (el tamaño del grupo es igual al producto de los tamaños de los subgrupos)
        2 - H ∩ K = {e}  (la intersección de los subgrupos es el conjunto que sólo tiene al elemento neutro)
        3 - ∀h ∈ H, ∀k ∈ K, h*k = k*h  (todos los elementos de un grupo conmutan con todos los del otro)
        El operador * es la operación del grupo G, que obtenemos de la tabla de Cayley, no está explícita.'''

		for par_hk in lista_de_pares_hk:
			H, K = par_hk[0], par_hk[1] # Desestructuramos el par en las variables H y K

			'''|H| * |K| = |G|'''
			if len(H) * len(K) != self.n: # self.n es |G|
				continue # Seguimos al siguiente par (H, K)

			'''H ∩ K = {e}'''
			if H.intersection(K) != neutro_set:
				continue # Seguimos al siguiente par (H, K)

			conmutan = True # Asumimos que conmutan, pero si encontramos un par que no lo haga, cambiamos a False
			'''∀h ∈ H, ∀k ∈ K, h*k = k*h'''
			for h in H:
				for k in K:
					if self.cayley[h][k] != self.cayley[k][h]:
						conmutan = False 
						break
				if not conmutan: # Al llegar aquí, se habrán recorrido todos los k para un h dado
					break
			'''Al llegar aquí, se habrán recorrido todos los h en H, por lo que, si conmutan sigue siendo True,
   			entonces ese par (H, K) cumple las 3 condiciones del producto interno.'''
			if not conmutan:
				continue

			print("El grupo SE PUEDE REPRESENTAR como producto interno de los subgrupos:")
			# Los sets en python no tienen orden, así que para que el print aparezca ordenado,
			# debemos convertir a lista y aplicar una función de ordenamiento:
			print(f"H = {sorted(list(H))}")
			print(f"K = {sorted(list(K))}")
			return
		print(f"NO se puede representar el grupo como producto interno de dos subgrupos.")
	
G = Grupo(3,[[0,1,2],[1,2,0],[2,0,1]])