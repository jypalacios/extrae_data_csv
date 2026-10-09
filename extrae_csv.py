import re
import pandas as pd

datos_procesados = []

# Abre tu archivo CSV original
with open("pacientes.csv", "r", encoding="utf-8") as f:
    # Nos saltamos la primera línea de la cabecera
    lineas = f.readlines()[1:]

    for linea in lineas:
        # 1. Buscamos el Teléfono (Cadena de 10 dígitos que empieza por 3)
        telefono_match = re.search(r",\s*(3\d{9})\s*,", linea)
        telefono = telefono_match.group(1) if telefono_match else None

        # 2. Buscamos la Edad (Número seguido de la palabra 'Años')
        edad_match = re.search(r",\s*(\d+)\s*Años\s*,", linea)
        edad = edad_match.group(1) if edad_match else None

        # 3. Buscamos la Identificación (Extrae solo los números omitiendo CC, CE, etc.)
        id_match = re.search(r",\s*(?:CC|CE|TI|PAS)?\s*(\d+)\s*,[^,]*3\d{9}", linea)
        identificacion = id_match.group(1) if id_match else None

        # 4. Buscamos el Paciente completo
        paciente_match = re.search(r",\s*([A-ZÑ\s]+),\s*(?:CC|CE|TI|PAS)?\s*\d+", linea)
        
        apellido = None
        nombre = None
        
        if paciente_match:
            paciente_completo = paciente_match.group(1).strip()
            # Dividimos el texto por espacios en blanco
            partes = paciente_completo.split()
            
            # Si tiene al menos 3 palabras (Ej: GORDILLO TOVAR GUILLERMO)
            if len(partes) >= 3:
                apellido = f"{partes[0]} {partes[1]}"  # Las dos primeras partes
                nombre = " ".join(partes[2:])          # Todo lo demás es el nombre
            # Caso de emergencia si solo tiene dos palabras (Ej: GORDILLO GUILLERMO)
            elif len(partes) == 2:
                apellido = partes[0]
                nombre = partes[1]
            else:
                apellido = paciente_completo
                nombre = ""

        # 5. Buscamos el Médico (Texto en mayúsculas después del campo de Edad)
        medico_match = re.search(r"Años\s*,\s*,*\s*([A-ZÑ\s]+),", linea)
        medico = medico_match.group(1).strip() if medico_match else None

        # Guardamos la información si logramos procesar la línea
        if identificacion or telefono:
            datos_procesados.append({
                "Apellido": apellido,
                "Nombre": nombre,
                "Identificacion": identificacion,
                "Edad": edad,
                "Telefono": telefono,
                "Medico": medico
            })

# Creamos el DataFrame estructurado de Pandas
df_final = pd.DataFrame(datos_procesados)

# Imprimimos las primeras filas para verificar el resultado
print(df_final.head())


#Extrae los campos
#df = df[fields] #Selecciona las columnas que se encuentran en el archivo csv    
#Guarda los campos en un archivo csv
df_final.to_csv('pacientes_extraidos.csv', index=False)
#df.to_csv('pacientes_extraidos.csv', index=False)
