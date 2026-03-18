# =========================
# Datos de entrada (ejemplo)
# =========================

interactions = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+")
]

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


# =========================================
# Generación de la salida
# =========================================

# Encabezado
print("TF\tTotal genes\tActivados\tReprimidos\tTipo")

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

    # imprimir resultado
    print(TF, total, activados, reprimidos, tipo, lista_genes, sep="\t")