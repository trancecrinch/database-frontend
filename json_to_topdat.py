import sys
import json
import re

# Documentation link below
# https://dna.physics.ox.ac.uk/index.php/Documentation#Configuration_file
# input .json file into command line
# print(sys.argv[1])

dat = open("out.dat", "w+")
top = open("out.top", "w+")

# if the file name ends with .json (some basic check)
if sys.argv[1].endswith('.json'):
    # with open(sys.argv[1], 'r') as json:
    # parsed_json = json.loads(sys.argv[1])
    # print(json.dumps(parsed_json, indent=4, sort_keys=True))

    # we will open user input with open('r') to read
    # and parse through the file with json.loads(f.read())
    # parsed_json is now wholly printable, 'pretty' print available with 
    # print(json.dumps(parsed_json, indent=4, sort_keys=True))
    f = open(sys.argv[1], "r")
    parsed_json = json.loads(f.read())

    # for heirarchy0 (h0) in parsed_json (same thing as just getting each line;
    # the file only should have 2 + the strand#s of lines. )
    # line1: dictionary of info
    # line2: dictionary of conf
    # line3+: dictionaries of strand#s

    for h0 in parsed_json:
        # print("%s: %s" % (h0, parsed_json[h0]))

        # prints out dict + key of the outermost layer
        # print('dict', h0)

        # first line of .top file:
        # 'info' holds: 
        # N Ns
        # N = count
        # Ns = strands
        # data['info'].append({
        #     'count': top[0].split(" ")[0],
        #     'strands': top[0].split(" ")[1]
        # })
        if 'info' in h0:
            # print('info')
            for h1 in parsed_json[h0]:
                top.write(h1['count'])
                top.write(" ")
                top.write(h1['strands'])
                top.write("\n")
                # for h2 in h1:
                #     # extracts N Ns
                #     # print(h1[h2])
                #     top.write(h1[h2])
                #     top.write(" ")
                # top.write("\n")
        
        # line 1-3 of .dat file
        # t b E
        # t = T
        # b = Lz Ly Lz
        # E = Etot U K
        # data['conf'].append({
        #     't': dat[0].split(" ")[2],
        #     'b': dat[1].split(" ")[2:5],
        #     'E': dat[2].split(" ")[2:5]
        # })
        if 'conf' in h0:
            # print('conf')
            for h1 in parsed_json[h0]:
                for h2 in h1: 
                    if 't' in h2:
                        # since t should not be treated as a list, we handle it separately
                        dat.write(h2)
                        dat.write(" = ")
                        dat.write(h1[h2])
                    else:
                        dat.write(h2)
                        dat.write(" = ")
                        for i in range(len(h1[h2])):
                            dat.write(h1[h2][i])
                            dat.write(" ")
                    dat.write("\n")
        
        # if on a strand#, 
        if 'strand' in h0: 
            # split the text into strand + number with regex
            # + indicates 1 or more matches
            # 
            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            strandindextuple = temp.match(h0).groups()
            # strandindextuple is a tuple of ('strand', 'index')
            # where 'index' is a number
            #
            # thus, print(strandindextuple[1]) will return back the index

            # print strand #
            # print(h0)

            for h1 in parsed_json[h0]:
                
                # data['strand' + s].append({
                #     'strandIndex': s,
                #     'externalindex': totalindex,
                #     'internalindex': index,
                #     'base': b,
                #     'add': '',
                #     'p3': p3,
                #     'p5': p5,
                #     'position': (rx, ry, rz),
                #     'backbone-base versor': (bx, by, bz),
                #     'normal versor': (nx, ny, nz), 
                #     'velocity': (vx, vy, vz),
                #     'angular velocity': (lx, ly, lz)
                # })

                # write to the .top file
                top.write(strandindextuple[1])
                top.write(" ")
                top.write(h1['base'])
                top.write(" ")
                top.write(h1['p3'])
                top.write(" ")
                top.write(h1['p5'])
                top.write("\n")

                # write to the .dat file
                for i in range(len(h1['position'])):
                    dat.write(h1['position'][i])
                    dat.write(" ")
                for i in range(len(h1['backbone-base versor'])):
                    dat.write(h1['backbone-base versor'][i])
                    dat.write(" ")
                for i in range(len(h1['normal versor'])):
                    dat.write(h1['normal versor'][i])
                    dat.write(" ")
                for i in range(0, 3):
                # for i in range(len(h1['velocity'])):
                    # dat.write(h1['velocity'][i])
                    dat.write("0")
                    dat.write(" ")
                for i in range(0, 3):
                # for i in range(len(h1['angular velocity'])):
                    # dat.write(h1['angular velocity'][i])
                    dat.write("0")
                    dat.write(" ")
                dat.write("\n")
                
    
    # print(json.dumps(parsed_json, indent=4, sort_keys=True))

# close off the file writing
dat.close()
top.close()