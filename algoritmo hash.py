import hashlib
import json

def generar_hash(objeto, algoritmo="sha256"):
    """
    Genera el hash de un objeto dado utilizando MD5 o SHA-256.
    
    :param objeto: Cualquier objeto serializable (diccionario, lista, cadena, etc.).
    :param algoritmo: Algoritmo de hash a utilizar ("md5" o "sha256").
    :return: Hash en formato hexadecimal.
    """
    # Convertir el objeto a una cadena JSON ordenada para garantizar consistencia
    objeto_serializado = json.dumps(objeto, sort_keys=True).encode('utf-8')
    
    # Seleccionar el algoritmo de hash
    if algoritmo == "md5":
        hash_obj = hashlib.md5()
    elif algoritmo == "sha256":
        hash_obj = hashlib.sha256()
    else:
        raise ValueError("Algoritmo no soportado. Usa 'md5' o 'sha256'.")
    
    # Calcular el hash
    hash_obj.update(objeto_serializado)
    return hash_obj.hexdigest()

# Ejemplo de uso
datos = {"usuario": "Juan", "id": 123, "saldo": 2500.75}

hash_md5 = generar_hash(datos, "md5")
hash_sha256 = generar_hash(datos, "sha256")

print("MD5:", hash_md5)
print("SHA-256:", hash_sha256)
