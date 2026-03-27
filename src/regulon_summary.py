import os

# =========================================
# Lectura del archivo y construcción de interactions
# =========================================

interactions = []

filename = "data/raw/NetworkRegulatorGene.tsv"

if not os.path.exists(filename):
    print("Error: archivo no encontrado")
    exit(1)
else:
    with open(filename) as f:        
        for line in f:
            
            line = line.strip()

            # Ignorar líneas vacías
            if not line:
                continue

            # Ignorar comentarios
            if line.startswith("#"):
                continue

            # Ignorar encabezado
            if line.startswith("1)regulatorId"):
                continue
            
            fields = line.split("\t")

            # Validar número mínimo de columnas
            if len(fields) <= 6:
                continue
                        
            TF = fields[1]
            gene = fields[4]
            effect = fields[5]

            # Validar effect
            if effect not in ["+", "-","+-"]:
                continue

            interactions.append((TF, gene, effect))


# =========================================
# Construcción del regulon con información extra
# =========================================

regulon = {}

for TF, gene, effect in interactions:
    
    # Inicializar estructura si el TF no existe
    if TF not in regulon:
        regulon[TF] = {
            "genes": [],
            "activados": 0,
            "reprimidos": 0
        }

    # Agregar gen a la lista
    regulon[TF]["genes"].append(gene)

    # Contar tipo de regulación
    if effect == "+":
        regulon[TF]["activados"] += 1
    elif effect == "-":
        regulon[TF]["reprimidos"] += 1
    elif effect == "+-":
        regulon[TF]["activados"] += 1
        regulon[TF]["reprimidos"] += 1  


# =========================================
# Generación de la salida
# =========================================

output_file = "results/regulon_summary.tsv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w") as out:
    out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes\n")

    for TF in sorted(regulon):
        
        # Obtener datos
        genes = sorted(regulon[TF]["genes"])
        total = len(genes)
        activados = regulon[TF]["activados"]
        reprimidos = regulon[TF]["reprimidos"]

        # Determinar tipo de regulación
        if activados > 0 and reprimidos > 0:
            tipo = "dual"
        elif activados > 0:
            tipo = "activador"
        else:
            tipo = "represor"

        lista_genes = ", ".join(genes)
        out.write(f"{TF}\t{total}\t{activados}\t{reprimidos}\t{tipo}\t{lista_genes}\n")
