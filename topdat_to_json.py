import sys
import json

# Documentation link below
# Usage: 
# python topdat-to-json.py <filename.dat> <filename.top>
# Will output a .json file with the following documentation: 
# <insert link here>
# https://dna.physics.ox.ac.uk/index.php/Documentation#Configuration_file
# Organizes the right files, doesn't matter which order you supply .dat and .top file
if sys.argv[1].endswith('.dat'):
    with open(sys.argv[1], 'r') as dat:
        dat = dat.read().splitlines()
    with open(sys.argv[2], 'r') as top:
        top = top.read().splitlines()
else:
    with open(sys.argv[2], 'r') as dat:
        dat = dat.read().splitlines()
    with open(sys.argv[1], 'r') as top:
        top = top.read().splitlines()

# Topology file (.top)
# Tuple: S B 3' 5'
# S = strandIndex
# B = bases
# 3' = p3
# 5' = p5

# strandIndex = []
# bases = []
# p3 = []
# p5 = []

# Configuration file (.dat)
# Tuple: Position, Backbone-base versor, Normal versor, Velocity, Angular velocity
# Position = position rx ry rz
# Backbone-base versor = backbone
# Normal versor = normal
# Velocity = velocity
# Angular velocity = angularVelocity

# first line in topology is total Nucleotides, number of strands N
# N Ns

# creates an array of topdat (each non-initialization entry of top concatenated with each of dat)
topdat = []
for i in range(len(top[1:])):
    topdat.append(top[i + 1] + " " + dat[i + 3][0:-1])

# sets up a data dict object
data = {}
data['info'] = []
data['conf'] = []

# line 1 of .top file
# N Ns
# N = count
# Ns = strands
data['info'].append({
    'count': top[0].split(" ")[0],
    'strands': top[0].split(" ")[1]
})

# line 1-3 of .dat file
# t b E
# t = T
# b = Lz Ly Lz
# E = Etot U K
data['conf'].append({
    't': dat[0].split(" ")[2],
    'b': dat[1].split(" ")[2:5],
    'E': [format(float(dat[2].split(" ")[i]), '.7f') for i in range(2, 5)]
})

strands = []
# initialize an index of the nucleotide within the current strand
# initialize a total index of the nucleotide within the entire structure
index = 0
totalindex = 0
# Split lines into each part
for lines in topdat: 
    # print(lines)
    s, b, p3, p5, rx, ry, rz, bx, by, bz, nx, ny, nz, vx, vy, vz, lx, ly, lz = lines.split(" ")
    # add to the internal index
    
    
    # check to see if a new strand is listed! 
    if s not in strands:
        strands.append(s)
        # create a dict with the strand number
        data['strand' + s] = []
        # reset the index if we're on a new strand
        index = 0
    data['strand' + s].append({
    # 'strandIndex': s,
    'externalindex': totalindex,
    'internalindex': index,
    'base': b,
    'add': '',
    'p3': p3,
    'p5': p5,
    'position': (format(float(rx), '.7f'), format(float(ry), '.7f'), format(float(rz), '.7f')),
    'backbone-base versor': (format(float(bx), '.7f'), format(float(by), '.7f'), format(float(bz), '.7f')),
    'normal versor': (format(float(nx), '.7f'), format(float(ny), '.7f'), format(float(nz), '.7f')), 
    # 'velocity': (vx, vy, vz),
    # 'angular velocity': (lx, ly, lz)
    })
    index += 1
    totalindex += 1
    
# creates a .json file with one of the file names
with open(sys.argv[1].split(".")[0] + ".json", "w+") as output:
    json.dump(data, output)