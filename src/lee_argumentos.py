import argparse

parser = argparse.ArgumentParser(
    description="Resumen de regulones a partir de un archivo TSV."
)

# definir argumentos
parser.add_argument(
    "input_file", help="Archivo TSV de entrada con interacciones TF-gene"
)
parser.add_argument(
    "output_file", help="Archivo TSV de salida con resumen de regulones"
)

parser.add_argument(
    "--min_genes",
    type=int,
    default=1,
    required=True,
    help="Número mínimo de genes regulados para incluir un TF",
)

args = parser.parse_args()

print(args)

print(f"Archivo de entrada: {args.input_file}")
print(f"Archivo de salida: {args.output_file}")
print(f"Número mínimo de genes regulados: {args.min_genes}")
