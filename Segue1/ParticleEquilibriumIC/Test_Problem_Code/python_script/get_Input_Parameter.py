import argparse

# load the command-line parameters
parser = argparse.ArgumentParser( description='Projection of mass density' )

parser = argparse.ArgumentParser()
parser.add_argument(
    "-N",
    "--number",
    type=int,
    required=True,
    help="Set NX0_TOT_X/Y/Z"
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    default="Input__Parameter.template"
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="Input__Parameter"
)

args=parser.parse_args()

with open(args.input, "r") as f:
    content = f.read()

content = content.replace("{N_python_replace}", str(args.number))

ExtPot_Path = f"ExtPotTable_{args.number}"
content = content.replace("{ExtPotTable_N_python_replace}", ExtPot_Path)

with open(args.output, "w") as f:
    f.write(content)