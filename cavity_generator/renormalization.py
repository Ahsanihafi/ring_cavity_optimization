import numpy as np
import matplotlib.pyplot as plt
parameter = np.loadtxt('normalization.csv', delimiter=',')

#ini nanti namanya diganti kali ya. jangan pakai istilah w_inter. Kemudian dibikin urut juga.
y0_min = parameter[0]
xinter_min = parameter[1]
y1_min = parameter[2]
x4_min = parameter[3]
y4_min = parameter[4]
y5_min = parameter[5]
w0_min = parameter[6]
winter_min = parameter[7]
w1_min = parameter[8]
w4_min = parameter[9]
y0_max = parameter[10]
xinter_max = parameter[11]
y1_max = parameter[12]
x4_max = parameter[13]
y4_max = parameter[14]
y5_max = parameter[15]
w0_max = parameter[16]
winter_max = parameter[17]
w1_max = parameter[18]
w4_max = parameter[19]
#kemudian outputnya
freq_min = parameter[20]
maxE_min = parameter[21]
inv_shunt_min = parameter[22]
freq_max = parameter[23]
maxE_max = parameter[24]
inv_shunt_max = parameter[25]
#container for output file



for nomor in range(1,6):
    #kita perlu iterasi baris untuk membuang yang ketidakpastiannya besar
    sampel = np.loadtxt('output_population_%d.csv' %nomor, delimiter=',', skiprows = 1)
    tsampel = np.transpose(sampel)
    print("Nomor: ", nomor, "Individu pareto awal: ", len(tsampel[0]))
    counter = 0
    cy0 = []
    cxinter = []
    cy1 = []
    cx4 = []
    cy4 = []
    cy5 = []
    cw0 = []
    cwinter = []
    cw1 = []
    cw4 = []
    cfreq = []
    cmaxE = []
    cinv_shunt = []
    for i in range(len(tsampel[0])):
        #maxE_uncer = maxE_min + (maxE_max-maxE_min)*((tsampel[13][i]-0.1)/0.8)
        #inv_shunt_uncer = inv_shunt_min + (inv_shunt_max-inv_shunt_min)*((tsampel[14][i]-0.1)/0.8)
        #freq_uncer = freq_min + (freq_max - freq_min)*((tsampel[16][i]-0.1)/0.8)
        maxE_uncer = tsampel[13][i]
        inv_shunt_uncer = tsampel[14][i]
        freq_uncer = tsampel[16][i]
        print(maxE_uncer, inv_shunt_uncer, freq_uncer)
        if maxE_uncer < 0.01 and inv_shunt_uncer < 0.01 and freq_uncer < 0.01:
            counter = counter + 1
            y0 = tsampel[1][i]*(y0_max-y0_min) + y0_min; cy0.append(y0)
            xinter = tsampel[2][i]*(xinter_max-xinter_min) + xinter_min; cxinter.append(xinter)
            y1 = tsampel[3][i]*(y1_max-y1_min) + y1_min; cy1.append(y1)
            x4 = tsampel[4][i]*(x4_max-x4_min) + x4_min; cx4.append(x4)
            y4 = tsampel[5][i]*(y4_max-y4_min) + y4_min; cy4.append(y4)
            y5 = tsampel[6][i]*(y5_max-y5_min) + y5_min; cy5.append(y5)
            w0 = tsampel[7][i]*(w0_max-w0_min) + w0_min; cw0.append(w0)
            winter = tsampel[8][i]*(winter_max-winter_min) + winter_min; cwinter.append(winter)
            w1 = tsampel[9][i]*(w1_max-w1_min) + w1_min; cw1.append(w1)
            w4 = tsampel[10][i]*(w4_max-w4_min) + w4_min; cw4.append(w4)
            #untuk output agak beda sedikit
            maxE = maxE_min + (maxE_max-maxE_min)*((tsampel[11][i]-0.1)/0.8); cmaxE.append(maxE)
            inv_shunt = inv_shunt_min + (inv_shunt_max-inv_shunt_min)*((tsampel[12][i]-0.1)/0.8); cinv_shunt.append(inv_shunt)
            freq = freq_min + (freq_max - freq_min)*((tsampel[15][i]-0.1)/0.8); cfreq.append(freq)    
    renormalized_input = np.vstack([cy0,cxinter,cy1,cx4,cy4,cy5,cw0,cwinter,cw1,cw4,cfreq,cmaxE,cinv_shunt])
    renormalized_input = np.transpose(renormalized_input)
    print("Individu pareto akhir: ", counter)
    np.savetxt('renormalized_input_separated%d.csv' %nomor, renormalized_input, delimiter=',')
    plt.xlabel("MaxE/Vacc (normalized)")
    plt.ylabel("Inverse Shunt Impedance (normalized)")
    plt.title("Combined pareto fronts")
    plt.scatter(tsampel[11], tsampel[12], label='Pareto %d' %nomor)
    plt.legend()
    
