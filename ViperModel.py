ff = {  # CF = 0
        0  : 'D <= ~M',                 # Complement
        1  : 'Y <= Nxt; P <= M',        # JSR
        2  : 'D <= I_O[M]',             # I/O Read
        3  : 'D <= Dat[M]',             # Mem Read
        4  : 'D <= R + M; B <=  C',     # Add (extended precision, modulo 2^32)
        5  : 'D <= R + M; B <=  C; S <= V', # Add (Stop on oVerflow)
        6  : 'D <= R - M; B <= ~C',     # Sub (extended precision, modulo 2^32)
        7  : 'D <= R - M; B <= ~C; S <= V', # Sub (Stop on oVerflow)   
        8  : 'D <=   R ^  M',           # XOR
        9  : 'Y <=   R &  M',           # AND
        10 : 'D <= ~(R |  M)',          # NOR
        11 : 'D <=   R & ~M',           # clear bits
        12 : 'D <= shift/rot(R)',       # MF sets the operations
        13 : 'Rsvd, STOP <= 1',
        14 : 'Rsvd, STOP <= 1',
        15 : 'Rsvd, STOP <= 1',
        # CF = 1
        16 : 'D <= R - M; B <= (R <  M)',
        17 : 'D <= R - M; B <= (R >= M)',
        18 : 'D <= R - M; B <= (R == M)',
        19 : 'D <= R - M; B <= (R != M)',
        20 : 'D <= R - M; B <= (R <= M)',
        21 : 'D <= R - M; B <= (R >  M)',
        22 : 'D <= R - M; B <= (  ~C  )',
        23 : 'D <= R - M; B <= (   C  )',
        24 : 'D <= R - M; B <= (R <  M) | B',
        25 : 'D <= R - M; B <= (R >= M) | B',
        26 : 'D <= R - M; B <= (R == M) | B',
        27 : 'D <= R - M; B <= (R != M) | B',
        28 : 'D <= R - M; B <= (R <= M) | B',
        29 : 'D <= R - M; B <= (R >  M) | B',
        30 : 'D <= R - M; B <= (  ~C  ) | B',
        31 : 'D <= R - M; B <= (   C  ) | B',
     }

width_ff = int(0)
width    = int(0)

for i in ff:
    width = len(ff[i])
    if width_ff < width:
        width_ff = width

df = {  0  : 'A <= D',
        1  : 'X <= D',
        2  : 'Y <= D',
        3  : 'P <= D',
        4  : 'P <= ( B) ? M : Nxt',
        5  : 'P <= (~B) ? M : Nxt',
        6  : 'I_O[M] <= D',             # I/O Write
        7  : 'Dat[M] <= D',             # Mem Write
     }

width_df = int(0)
width    = int(0)

for i in df:
    width = len(df[i])
    if width_df < width:
        width_df = width

rf = {  0  : 'R <= A',
        1  : 'R <= X',
        2  : 'R <= Y',
        3  : 'R <= P',
     }

width_rf = int(0)
width    = int(0)

for i in rf:
    width = len(rf[i])
    if width_rf < width:
        width_rf = width

mf = {  0  : 'M <=  KA',
        1  : 'M <= (KA)',
        2  : 'M <= (KA + X)',
        3  : 'M <= (KA + Y)',
     }

width_mf = int(0)
width    = int(0)

for i in mf:
    width = len(mf[i])
    if width_mf < width:
        width_mf = width

sf = {  0  : 'D <= R >>> 1; R[31] <= R[31]; B <= R[ 0]',
        1  : 'D <= R >>  1; R[31] <= B;     B <= R[ 0]',
        2  : 'D <= R <<< 1; R[ 0] <= B;     B <= R[31]; S <= V',
        3  : 'D <= R <<  1; R[ 0] <= B;     B <= R[31]',
     }

width_sf = int(0)
width    = int(0)

for i in sf:
    width = len(sf[i])
    if width_sf < width:
        width_sf = width

if width_sf < width_ff:
    width_sf = width_ff
else: width_ff = width_sf

print(width_ff, width_df, width_rf, width_mf, width_sf, end='')

idx = int(0)
instructions = list()
numInstructions = [0] * 32
ff_idx = int(0)

with open('ViperInstructionTbl.txt', 'wt') as fout:
    ff_idx = 0
    for i in ff:
        for j in df:
            for k in rf:
                for l in mf:
                    if i < 2048: cf = False
                    
                    idx_ff = bin(i)[2:]
                    if len(idx_ff) < 5:
                        idx_ff = '0'*(5-len(idx_ff)) + idx_ff

                    idx_df = bin(j)[2:]
                    if len(idx_df) < 3:
                        idx_df = '0'*(3-len(idx_df)) + idx_df

                    idx_rf = bin(k)[2:]
                    if len(idx_rf) < 2:
                        idx_rf = '0'*(2-len(idx_rf)) + idx_rf

                    idx_mf = bin(l)[2:]
                    if len(idx_mf) < 2:
                        idx_mf = '0'*(2-len(idx_mf)) + idx_mf

                    if cf is False:
                        if (i == 0):    # D <= ~M
                            if ((j == 0) and (k == 0)) or \
                               ((j == 1) and (k == 1) and (l != 2)) or \
                               ((j == 2) and (k == 2) and (l != 3)) or \
                               ((j == 4) and (k == 3)             ) or \
                               ((j == 5) and (k == 3)             ) or \
                               ((j == 6) and (l != 0) and \
                                ((k == 0) or \
                                 ((k == 1) and (l != 2)) or \
                                 ((k == 2) and (l != 3)) ) ) or \
                               ((j == 7) and (l != 0) and \
                                (((k == 0) or  (k == 3)) or \
                                 ((k == 1) and (l != 2)) or \
                                 ((k == 2) and (l != 3)) ) ): err = False
                            else: err = True
                        elif (i == 1):  # Y <= P + 1, P <= M (JSR)
                            if ((j == 3) and (k == 3)): err = False
                            else: err = True
                        elif (i == 2):  #GET
                            if (  (l != 0) and \
                                (((j == 1) and (k == 1) and (l != 2)) or \
                                 ((j == 2) and (k == 2) and (l != 3)) or \
                                 ((j == 0) and (k == 0)) ) ): err = False
                            else: err = True
                        elif (i == 3):  #LDA
                            if ((j == 0) and (k == 0)) or \
                               ((j == 1) and (k == 1) and (l != 2)) or \
                               ((j == 2) and (k == 2) and (l != 3)) or \
                               ((j == 3) and (k == 3)             ): err = False
                            else: err = True
                        elif (i == 4):  # D <= R + M, B <= Co
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 5):  # D <= R + M, STOP <= V
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 3):
                                if (l != 0) or (k != 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 6):  # D <= R - M, B <= ~Co
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 7):  # D <= R - M, STOP <= V
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 3):
                                if (l != 0) or (k != 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 8):  # D <= R ^ M
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 9):  # D <= R & M
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 10): # D <= ~(R | M)
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 11): # D <= R & ~M
                            if (j == 0):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 1):
                                if (k == 1) and (l == 2): err = True
                                elif (k == 3): err = True
                                else: err = False
                            elif (j == 2):
                                if (k == 2) and (l == 3): err = True
                                elif (k == 3): err = True
                                else: err = False
                            else: err = True
                        elif (i == 12): # D <= Shift/Rotate(R)
                            if ((j == 0) or (j == 1) or (j == 2)) and \
                                (k != 3): err = False
                            else: err = True
                        elif (i == 13): # Reserved, STOP <= 1
                            err = True
                        elif (i == 14): # Reserved, STOP <= 1
                            err = True
                        elif (i == 15): # Reserved, STOP <= 1
                            err = True
                        elif (i > 15):  # Comparison Instructions
                            if ((j == 1) and (k == 1) and (l != 2)) or \
                               ((j == 2) and (k == 2) and (l != 3)) or \
                               ((j == 0) and (k == 0)): err = False
                            else: err = True
                        else:
                            err = True

                    if ((i == 0) and ((j == 6) or (j == 7)) ):
                        line = '0x%03X' % (idx)                       + \
                               ',%1s_%4s_%3s_%2s_%2s' % (idx_ff[0],
                                                         idx_ff[1:],
                                                         idx_df,
                                                         idx_rf,
                                                         idx_mf     ) + \
                                ',%-1s' % (str(err)[0])               + \
                                ',%-*s' % (width_df, df[j])           + \
                                ',%-*s' % (width_ff, 'D <= R')        + \
                                ',%-*s' % (width_rf, rf[k])           + \
                                ',%-*s' % (width_mf, mf[l])
                        print(line, file=fout)
                    elif (i == 12):
                        line = '0x%03X' % (idx)                       + \
                               ',%1s_%4s_%3s_%2s_%2s' % (idx_ff[0],
                                                         idx_ff[1:],
                                                         idx_df,
                                                         idx_rf,
                                                         idx_mf     ) + \
                                ',%-1s' % (str(err)[0])               + \
                                ',%-*s' % (width_df, df[j])           + \
                                ',%-*s' % (width_sf, sf[l])           + \
                                ',%-*s' % (width_rf, rf[k])
                        print(line, file=fout)
                    else:
                        line = '0x%03X' % (idx)                       + \
                               ',%1s_%4s_%3s_%2s_%2s' % (idx_ff[0],
                                                         idx_ff[1:],
                                                         idx_df,
                                                         idx_rf,
                                                         idx_mf     ) + \
                                ',%-1s' % (str(err)[0])               + \
                                ',%-*s' % (width_df, df[j])           + \
                                ',%-*s' % (width_ff, ff[i])           + \
                                ',%-*s' % (width_rf, rf[k])           + \
                                ',%-*s' % (width_mf, mf[l])
                        print(line, file=fout)

                    if err == False:
                        numInstructions[ff_idx] += 1
                        instructions.append(line)
                    idx += 1
                    
        ff_idx += 1

sum = int(0)
for i in numInstructions:
    sum += i
  
print('', numInstructions, sum)
        
with open('ViperInstructionSet.txt', 'wt') as fout:
    for instruction in instructions:
        flds = instruction.split(',')
        if len(flds) == 7:
            hexCode, binCode, err, src, aluOp, dst, mem = flds
        else:
            hexCode, binCode, err, src, cmpOp, dst = flds
            

        cond, alu, dst, src, addr = binCode.split('_')

        CF = int(cond, 2)
        FF = int(alu, 2)
        DF = int(dst, 2)
        RF = int(src, 2)
        MF = int(addr, 2)

        if CF == 0:
            if FF == 0:
                if DF >= 0 and DF <= 2:
                    if DF == 0: reg = 'A'
                    elif DF == 1: reg = 'X'
                    else: reg = 'Y'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'LDC'
                    print(hexCode, binCode, '%-6s%1s,%-s' % \
                                            (opcode, reg, adrMode), \
                          file = fout)
                elif DF == 4:
                    opcode = 'JBS'

                    if MF == 0:
                        adrMode = 'rel'
                        opcode = 'BBS'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    print(hexCode, binCode, '%-6s%-s' % (opcode, adrMode), \
                          file = fout)
                elif DF == 5:
                    opcode = 'JBC'

                    if MF == 0:
                        adrMode = 'rel'
                        opcode = 'BBC'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    print(hexCode, binCode, '%-6s%-s' % (opcode, adrMode), \
                          file = fout)
                elif DF == 6:
                    if RF == 0: reg = 'A'
                    elif RF == 1: reg = 'X'
                    else: reg = 'Y'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'PUT'

                    print(hexCode, binCode, '%-6s%1s,%-s' % \
                                            (opcode, reg, adrMode), \
                          file = fout)
                elif DF == 7:
                    if RF == 0: reg = 'A'
                    elif RF == 1: reg = 'X'
                    elif RF == 2: reg = 'Y'
                    else: reg = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'STA'

                    print(hexCode, binCode, '%-6s%1s,%-s' % \
                                            (opcode, reg, adrMode), \
                          file = fout)
                else: print(hexCode, binCode, 'Unhandled instruction *********')
            elif FF == 1:
                    opcode = 'JSR'
                    
                    if MF == 0:
                        adrMode = 'rel'
                        opcode = 'BSR'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    print(hexCode, binCode, '%-6s%-s' % (opcode, adrMode), \
                          file = fout)
            elif FF == 2:
                    if RF == 0: reg = 'A'
                    elif RF == 1: reg = 'X'
                    elif RF == 2: reg = 'Y'
                    else: reg = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'GET'
                    
                    print(hexCode, binCode, '%-6s%1s,%-s' % \
                                            (opcode, reg, adrMode), \
                          file = fout)
            elif FF == 3:
                    if RF == 0: reg = 'A'
                    elif RF == 1: reg = 'X'
                    elif RF == 2: reg = 'Y'
                    else: reg = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    if RF == 3:
                        opcode = 'JMP'
                        if MF == 0:
                            adrMode = 'rel'
                            opcode = 'BRA'
                        print(hexCode, binCode, '%-6s%-s' % \
                                                (opcode, adrMode), \
                              file = fout)
                    else:
                        opcode = 'LDA'
                        print(hexCode, binCode, '%-6s%1s,%-s' % \
                                                (opcode, reg, adrMode), \
                              file = fout)
            elif FF == 4:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'ADD'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode), \
                          file = fout)
            elif FF == 5:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    if DF == 3:
                        opcode = 'BRF'
                        print(hexCode, binCode, '%-6s%-s' % \
                                                (opcode, 'rel'), \
                              file = fout)
                    else:
                        opcode = 'ADDS'
                        print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                                (opcode, dst, src, adrMode), \
                              file = fout)
            elif FF == 6:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'SUB'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode), \
                          file = fout)
            elif FF == 7:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    if DF == 3:
                        opcode = 'BRR'
                        print(hexCode, binCode, '%-6s%-s' % \
                                                (opcode, 'rel'), \
                              file = fout)
                    else:
                        opcode = 'SUBS'
                        print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                                (opcode, dst, src, adrMode), \
                              file = fout)
            elif FF == 8:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'XOR'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode), \
                          file = fout)
            elif FF == 9:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'ORL'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode),
                          file = fout)
            elif FF == 10:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'NOR'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode), \
                          file = fout)
            elif FF == 11:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: adrMode = '#imm'
                    elif MF == 1: adrMode = 'abs'
                    elif MF == 2: adrMode = 'abs+X'
                    else: adrMode = 'abs+Y'

                    opcode = 'BIC'
                    
                    print(hexCode, binCode, '%-6s%1s,%1s,%-s' % \
                                            (opcode, dst, src, adrMode), \
                          file = fout)
            elif FF == 12:
                    if RF == 0: src = 'A'
                    elif RF == 1: src = 'X'
                    elif RF == 2: src = 'Y'
                    else: src = 'P'

                    if DF == 0: dst = 'A'
                    elif DF == 1: dst = 'X'
                    elif DF == 2: dst = 'Y'
                    else: dst = 'P'

                    if MF == 0: opcode = 'ASR'
                    elif MF == 1: opcode = 'ROR'
                    elif MF == 2: opcode = 'ASL'
                    else: opcode = 'ROL'

                    print(hexCode, binCode, '%-6s%1s,%1s' % \
                                            (opcode, dst, src), \
                          file = fout)
            else: print(hexCode, binCode, 'Unhandled intstruction ************')
        else:
            if RF == 0: src = 'A'
            elif RF == 1: src = 'X'
            elif RF == 2: src = 'Y'
            else: src = 'P'

            if MF == 0: adrMode = '#imm'
            elif MF == 1: adrMode = 'abs'
            elif MF == 2: adrMode = 'abs+X'
            else: adrMode = 'abs+Y'

            if FF == 0:    cc = 'LT'
            elif FF ==  1: cc = 'GE'
            elif FF ==  2: cc = 'EQ'
            elif FF ==  3: cc = 'NE'
            elif FF ==  4: cc = 'LE'
            elif FF ==  5: cc = 'GT'
            elif FF ==  6: cc = 'LS'
            elif FF ==  7: cc = 'HI'
            elif FF ==  8: cc = 'LT'
            elif FF ==  9: cc = 'GE'
            elif FF == 10: cc = 'EQ'
            elif FF == 11: cc = 'NE'
            elif FF == 12: cc = 'LE'
            elif FF == 13: cc = 'GT'
            elif FF == 14: cc = 'LS'
            else:          cc = 'HI'

            opcode = 'SEB' if (FF >= 0) and (FF < 8) else 'ORB'

            print(hexCode, binCode, '%-6s%1s,%1s,%1s' % \
                                    (opcode, cc, src, adrMode), \
                  file = fout)
            
            
