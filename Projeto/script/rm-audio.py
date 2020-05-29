import argparse
import os

# usando o argparser para a linha de comando

psr = argparse.ArgumentParser(description="""
	  Script para remover todas as trilhas de áudio de um ou mais vídeos.""",
	  formatter_class=argparse.RawDescriptionHelpFormatter
)

psr.add_argument("vca", help="Caminho do diretório com os vídeos.")
psr.add_argument("vsa", help="Caminho para guardar os vídeos sem áudio.")
psr.add_argument("-ev", default="mp4", help="Extensão dos vídeos. (default=mp4)")

args = psr.parse_args()

# removendo o áudio dos vídeos e salvando-os

os.chdir(args.vca)
vids = [v for v in os.listdir() if v.endswith("."+args.ev)]
vids.sort()

for v in vids:
	vsa = args.vsa+"/" if not args.vsa.endswith("/") else args.vsa
	novo = vsa + v
	com = "ffmpeg -i {vca} -an {vsa}".format(vca=v, vsa=novo)
	os.system(com)
