import argparse
import os

# definicao dos parametros da linha de comando

parser = argparse.ArgumentParser(description="""
	Script para extrair frames de um ou mais vídeos-fonte.""",
	formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument("pv", help="Caminho do diretório dos vídeos.")
parser.add_argument("-ev", default="mp4", help="Extensão dos vídeos. (default=mp4)")
parser.add_argument("-p", type=int, help="Primeiro vídeo a ser analisado.")
parser.add_argument("-u", type=int, help="Último vídeo a ser analisado.")
parser.add_argument("-ss", type=float, default=2.0, help="Offset do início do vídeo. (default=2.0)")
parser.add_argument("-r", type=float, default=1.5, help="Frames a serem extraídos por segundo. (default=1.5)")
parser.add_argument("-ef", default="jpg", help="Extensão dos frames extraídos. (default=jpg)")
parser.add_argument("-q", default=1, help="Qualidade dos frames extraídos. (default=1)")
parser.add_argument("pf", help="Caminho do diretório dos frames.")

# coleta parametros da linha de comando

args = parser.parse_args()

# lista de videos a serem analisados

vids = [v for v in os.listdir(args.pv) if v.endswith("."+args.ev)]
vids.sort()

# script de extracao das frames

for v in vids:
	num = int(v[v.find("-")+1:v.find(".")])
	if (args.p is None or args.p <= num) and (args.u is None or num <= args.u):
		pref = v[:v.find(".")]
		com = "ffmpeg -i {}/{} -ss {} -r {} -q:v {} {}/{}-%03d.{}"\
			  .format(args.pv, v, args.ss, args.r,
			  		  args.q, args.pf, pref, args.ef)
		os.system(com)

# geralmente os dois primeiros frames do video sao muito parecidos
# assim, exclui-se o primeiro frame de cada video

os.chdir(args.pf)

arqs = os.listdir()
arqs.sort()

toDel = []
for f in arqs:
	if f.endswith("-001." + args.ef):
		toDel.append(f)
for f in toDel:
	os.remove(f)

# renomear os arquivos para compensar a falta dos arquivos 001

arqs = os.listdir()
arqs.sort()

for f in arqs:
	num = int(f[f.rfind("-")+1:f.rfind(".")])
	rep = f[f.rfind("-")+1:]
	pred = str(num-1).zfill(3) + "." + args.ef
	new = f.replace(rep, pred)
	os.rename(f, new)
