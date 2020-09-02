#!/usr/bin/python3
##    This file is part of pyrlsdr.
from __future__ import division
from __future__ import print_function
from rtlsdr import *
import cmath
import math
from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Enter the frequency(Mhz):')
        self.lbl2=Label(win, text='SAR at frequency(Mhz) :')
        self.lbl3=Label(win, text='Cerebrospinal fluid:')
        self.lbl4=Label(win, text='EYE humar:')
        self.lbl5=Label(win, text='Liver bile:')
        self.lbl6=Label(win, text='Blood:')
        self.lbl7=Label(win, text='received power(dbm):')
        self.lbl8=Label(win, text='SAR at w/kg', fg='green', font=("Helvetica", 18))
        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.t3=Entry()
        self.t4=Entry()
        self.t5=Entry()
        self.t6=Entry()
        self.t7=Entry()
        self.btn1 = Button(win, text='Enter')
        self.lbl1.place(x=55, y=70)
        self.lbl2.place(x=55, y=150)
        self.lbl7.place(x=55, y=190)
        self.lbl8.place(x=55, y=230)
        self.lbl3.place(x=55, y=270)
        self.lbl4.place(x=55, y=300)
        self.lbl5.place(x=55, y=330)
        self.lbl6.place(x=55, y=360)
        self.t1.place(x=230, y=70)
        self.t2.place(x=230, y=150)
        self.t7.place(x=230, y=190)
        self.t3.place(x=230, y=270)
        self.t4.place(x=230, y=300)
        self.t5.place(x=230, y=330)
        self.t6.place(x=230, y=360)
        self.lbl=Label(window, text="Specific absorption rate calculations", fg='green', font=("Helvetica", 18))
        self.lbl.place(x=50, y=15)

        self.b1=Button(win, text='Enter', command=self.main)
        self.b1.place(x=350, y=100)

    def main(self):
        num1=int(self.t1.get())
        result=num1
        en_freq=num1*1e6
        @limit_calls(2)
        def test_callback(samples, rtlsdr_obj):
            print('  in callback')
            print('  signal mean:', sum(samples)/len(samples))

        sdr = RtlSdr()

        print('Configuring SDR...')
        sdr.rs = 2.4e6
        sdr.fc = en_freq
        sdr.gain = 19.2
        print('  sample rate: %0.6f MHz' % (sdr.rs/1e6))
        print('  center frequency %0.6f MHz' % (sdr.fc/1e6))
        print('  gain: %d dB' % sdr.gain)

        print('Reading samples...')
        samples = sdr.read_samples(256*1024)
        print('  signal mean:', sum(samples)/len(samples))

        print('Testing callback...')
        sdr.read_samples_async(test_callback, 256*1024)

        import pylab as mpl

        print('Testing spectrum plotting..')

        mpl.figure(1)

        power,freq = mpl.psd(samples, NFFT=1024, Fc=sdr.fc/1e6, Fs=sdr.rs/1e6)
        p = list(power)
        f = list(freq)
        frequency= f[p.index(max(p))]
        rec_power= 10*math.log10(max(p))/1
        print("Freq", frequency)
        self.t2.insert(END, float(frequency))
        self.t7.insert(END, float(rec_power))
        print("power", rec_power )
        val=abs(rec_power)
        print("density in dbm:",(val))
        import array as arr
        a = arr.array('d', [0.121,0.0960,0.0763,0.0606,0.0481,0.0382,0.0304,0.0241,0.0192,0.0152,
                            0.0121,0.00960,0.00763,0.00606,0.00481,0.00382,0.00304,0.00241,0.00192,
                            0.00152,0.00121,0.000960,0.000763,0.000606,0.000481,0.000382,0.000304,
                            0.000241,0.000192,0.000152,0.000121])
        i_avg=a[int(val)]
        print("i_avg",i_avg,"w/m2")
        c=3*1e8
        e0=8.85*1e-12
        print("val",c*e0)
        Erms=math.sqrt(i_avg/(c*e0))
        interm=math.sqrt(Erms*377)
        print("Erms :", interm,"v/m")
        MD=985.0 #mass density of a human body 985 kg/m^3
        con=arr.array('d',[2.41,1.50,1.40,0.70]) #conductivity of the materials (cerebrospinal fluid,eye humar,bile,blood)
        SAR=[0]*4
        cou=0
        while (cou <=3):
            SAR[cou]=(con[cou]*(interm*interm))/MD
            print("SAR level",cou,SAR)
            cou=cou + 1

        import matplotlib.pyplot as plt
        plt.figure(2)
        con=arr.array('d',[2.41,1.50,1.40,0.70]) #conductivity of the materials (cerebrospinal fluid,eye humar,bile,blood)

        # x-coordinates of left sides of bars
        left = [1, 2, 3, 4]

        # heights of bars
        i=0
        while(i<=3):
         hight=[SAR[0],SAR[1],SAR[2],SAR[3]]
         i=i+1

        # labels for bars
        self.t3.insert(END, float(SAR[0]))
        self.t4.insert(END, float(SAR[1]))
        self.t5.insert(END, float(SAR[2]))
        self.t6.insert(END, float(SAR[3]))
        tick_label = ['Cerebrospinal fluid', 'EYE humar', 'Liver bile', 'Blood']

        # plotting a bar chart

        plt.bar(left, hight, tick_label = tick_label,
                width = 0.5, color = ['r'])

        # naming the x-axis
        plt.xlabel('parts of Human body')
        # naming the y-axis
        plt.ylabel('SAR in w/kg')
        # plot title
        plt.title('RADIATION ABSORPTION PLOT')
        # function to show the plot
        mpl.show(1)
        plt.show(2)
window=Tk()
mywin=MyWindow(window)
window.title('SAR Calculation')
window.geometry("480x400+10+10")
window.mainloop()