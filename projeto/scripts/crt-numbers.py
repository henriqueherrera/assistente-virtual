import argparse
import os
from os import path

# funções utilitárias

getPfx = lambda a: a[:a.find("-")]
getn1 = lambda a: int(a[a.find("-")+1:a.rfind("-")])
getn2 = lambda a: int(a[a.rfind("-")+1:a.rfind(".")])
getExt = lambda a: a[a.rfind(".")+1:]

# obtendo argumentos da linha de comando

psr = argparse.ArgumentParser(description="""
	Script para corrigir a numeração dos arquivos
	quando há 'saltos' entre os números (ex.: 1, 2, 4, 5, 6, 9, ...)."""
)

psr.add_argument("p", help="Caminho dos arquivos.")

args = psr.parse_args()

p = args.p

# normalizando paths

p = path.abspath(path.expanduser(p))

# obtendo a lista de arquivos

os.chdir(p)
arqs = os.listdir()
arqs.sort()

# corrigindo a numeração

pfx = getPfx(arqs[0])
ext = getExt(arqs[0])

i1 = 0
i2 = 0
c = 0
while c < len(arqs):
	a = arqs[c]
	r1 = getn1(a)
	r2 = getn2(a)

	novo = "{}-{}-{}.{}".format(pfx, str(i1).zfill(3), str(i2).zfill(3), ext)
	ren = path.join(p, novo)
	os.rename(a, ren)

	c += 1

	if c < len(arqs):
		prox1 = getn1(arqs[c])
		if prox1 > r1:
			i1 += 1
			i2 = 0
		else:
			i2 += 1
