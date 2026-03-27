import os

# TODO: extraer este bloque a load_interactions(input_file)
# Debe reutilizar la lógica existente sin cambiar validaciones ni estructura de interactions.

def load_interactions(input_file):
    """Carga las interacciones del archivo TSV de reguladores a genes.

    Lee `input_file`, ignora comentarios (#), encabezado y filas inválidas.
    Valida que cada fila tenga al menos 7 columnas y efecto sea '+' o '-'.

    Args:
        input_file (str): Ruta al archivo TSV de entrada.

    Returns:
        list[tuple[str, str, str]]: Lista de tuplas (TF, gene, effect).

    Raises:
        SystemExit: Si el archivo no existe.
    """
    interactions = []

    if not os.path.exists(input_file):
        print("Error: archivo no encontrado")
        exit(1)
    else:
        with open(input_file) as f:
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
                if effect not in ["+", "-"]:
                    continue

                interactions.append((TF, gene, effect))

    return interactions


def build_regulon(interactions):
    """Construye la estructura de regulon a partir de interacciones validadas.

    Args:
        interactions (list[tuple[str, str, str]]): Lista de interacciones (TF, gen, efecto).

    Returns:
        dict: Diccionario con clave TF y valores {
            'genes': list[str],
            'activados': int,
            'reprimidos': int
        }.
    """
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

    return regulon


def get_regulator_type(activados, reprimidos):
    """Determina el tipo de regulador según el conteo de efectos.

    Args:
        activados (int): Número de genes activados.
        reprimidos (int): Número de genes reprimidos.

    Returns:
        str: "dual" si ambos >0, "activador" si solo activados >0, "represor" si solo reprimidos.
    """
    if activados > 0 and reprimidos > 0:
        return "dual"
    elif activados > 0:
        return "activador"
    else:
        return "represor"


def write_summary(regulon, output_file):
    """Escribe el resumen del regulon en un archivo TSV.

    Args:
        regulon (dict): Diccionario de regulon construído por build_regulon.
        output_file (str): Ruta de salida para el archivo TSV.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as out:
        out.write("TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes\n")

        for TF in sorted(regulon):
            genes = sorted(regulon[TF]["genes"])
            total = len(genes)
            activados = regulon[TF]["activados"]
            reprimidos = regulon[TF]["reprimidos"]

            tipo = get_regulator_type(activados, reprimidos)
            lista_genes = ", ".join(genes)
            out.write(f"{TF}\t{total}\t{activados}\t{reprimidos}\t{tipo}\t{lista_genes}\n")


def main():
    """Punto de entrada para la ejecución principal del script.

    Args:
        None

    Returns:
        None
    """
    input_file = "data/raw/NetworkRegulatorGene.tsv"
    output_file = "results/regulon_summary.tsv"

    interactions = load_interactions(input_file)
    regulon = build_regulon(interactions)
    write_summary(regulon, output_file)


if __name__ == "__main__":
    main()