import sys
import numpy as np
import serpentTools as sp
import csv

##Conditional Check
#keff check
res = sp.read('burnmodel_res.m')
if res.resdata['absKeff'][0][0] > 1.01 or res.resdata['absKeff'][3][0] < 0.99:
	sys.exit(23)

#burn check
initburn = [[2362, 6109, 4526, 2362, 4758, 6109, 6535, 4690, 2581, 5845, 4829]
           ,[6535, 6340, 4300, 6535, 4130, 2131, 3740, 5128, 3904, 3904, 3865]
           ,[2743, 3202, 3904, 4953, 7510, 6109, 3904, 5523, 2830, 1530, 1902]
           ,[5128, 4721, 1871, 6535, 5025, 3372, 5914, 3904, 6109, 3904, 0] 
           ,[6109, 3270, 4563, 2870, 6109, 3576, 1927, 2512, 3305, 5455, 0]
           ,[4563, 5877, 6925, 5914, 6340, 3904, 4762, 2581, 5419, 0, 0]
           ,[3536, 3904, 6340, 3904, 2199, 2512, 5224, 5224, 1595, 0, 0]
           ,[1428, 4136, 1541, 3904, 3904, 2812, 3904, 4331, 0, 0, 0]
           ,[5419, 2512, 5224, 2404, 6109, 1865, 5060, 0, 0, 0, 0]
           ,[3469, 5224, 3904, 2581, 3469, 3237, 0, 0, 0, 0, 0]
           ,[4598, 5455, 3904, 0, 0, 0, 0, 0, 0, 0, 0]]
channels2 = [['AA','BA','CA','DA','EA','FA','GA','HA','IA','JA','KA']
           ,['AB','BB','CB','DB','EB','FB','GB','HB','IB','JB','KB']
           ,['AC','BC','CC','DC','EC','FC','GC','HC','IC','JC','KC']
           ,['AD','BD','CD','DD','ED','FD','GD','HD','ID','JD', 0 ]
           ,['AE','BE','CE','DE','EE','FE','GE','HE','IE','JE', 0 ]
           ,['AF','BF','CF','DF','EF','FF','GF','HF','IF', 0 , 0 ]
           ,['AG','BG','CG','DG','EG','FG','GG','HG','IG', 0 , 0 ]
           ,['AH','BH','CH','DH','EH','FH','GH','HH', 0 , 0 , 0 ]
           ,['AI','BI','CI','DI','EI','FI','GI', 0 , 0 , 0 , 0 ]
           ,['AJ','BJ','CJ','DJ','EJ','FJ', 0 , 0 , 0 , 0 , 0 ]
           ,['AK','BK','CK', 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]]

file = '/home/aaronwb7/databurn/burnmodel_det3.m'
det2 = sp.read(file)
levals = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
f = open('history.csv','r')  
ref=[]
reads = csv.reader(f,delimiter=',')
for row in reads:
    ref.append(row)
f.close()
filelist = len(ref)
burn = np.zeros((filelist,11,11))
for ii in range(11):
        burn[0][ii][:] = det2.detectors['channelpowers'].tallies[levals[ii]]/1000000/0.265789*2.8
for ii in range(filelist):
    file2 = '/home/aaronwb7/databurn/burnmodel'+str(ii+1)+'_det3.m'
    det2 = sp.read(file2)
    for jj in range(11):
        burn[ii][jj][:] = det2.detectors['channelpowers'].tallies[levals[jj]]/1000000/0.265789*2.8     
chanburn = initburn
for ii in range(len(burn)):
    chanburn = chanburn + burn[ii][:][:]
    for jj in range(len(channels2)):
        for kk in range(len(channels2[jj])):
            if channels2[jj][kk] == ref[ii][0]:
                chanburn[jj][kk] = chanburn[jj][kk] * 0.3
                if ref[ii][1] == 'True' or ref[ii][1] == True or ref[ii][1] == 'TRUE':
                    for ll in range(len(channels2)):
                        for pp in range(len(channels2[ll])):
                            if channels2[ll][pp] == ref[ii][2]:
                                chanburn[ll][pp] = chanburn[ll][pp] * 0.3

indref1, indref2 = np.unravel_index(chanburn.argmax(), chanburn.shape)
refchan = channels2[indref1][indref2]
if chanburn[indref1,indref2] < 6000 or chanburn[indref1][indref2] > 7600:
	sys.exit(23)

k = open('flip.csv','r')
flip=[]
fliptemp = csv.reader(k)
for row in fliptemp:
	flip.append(row)
k.close()
refdir = flip[indref1][indref2]

channels = ['AA','BA','CA','DA','EA','FA','GA','HA','IA','JA','KA',
            'AB','BB','CB','DB','EB','FB','GB','HB','IB','JB','KB',
            'AC','BC','CC','DC','EC','FC','GC','HC','IC','JC','KC',
            'AD','BD','CD','DD','ED','FD','GD','HD','ID','JD',
            'AE','BE','CE','DE','EE','FE','GE','HE','IE','JE',
            'AF','BF','CF','DF','EF','FF','GF','HF','IF',
            'AG','BG','CG','DG','EG','FG','GG','HG','IG',
            'AH','BH','CH','DH','EH','FH','GH','HH',
            'AI','BI','CI','DI','EI','FI','GI',
            'AJ','BJ','CJ','DJ','EJ','FJ',
            'AK','BK','CK']

dep = sp.read('burnmodel_dep.m')

refuel = refchan
direction = refdir

###
second = False
ref2 = 'none'
direction2 = 'none'

if direction == 'front':
    buns = np.linspace(1,8,8,dtype=int)
elif direction == 'back':
    buns = np.linspace(5,12,8,dtype=int)
    
if direction2 == 'front':
    buns2 = np.linspace(1,8,8,dtype=int)
elif direction2 == 'back':
    buns2 = np.linspace(5,12,8,dtype=int)
	
fresh = ' 8016.09c  4.6375E-02\n 92234.09c  1.2751E-06\n 92235.09c  1.6687E-04\n 92238.09c  2.3014E-02\n'

#Create new fuelmat
#create list of isotope IDs
name = dep.metadata['zai']
for ii in range(len(name)):
    name[ii]=str(name[ii])   #int -> str
    if name[ii][-1] == '1':  #check if metastable
        l = list(name[ii])   #str -> list
        l[2] = '3'           #convert metastable
        name[ii]=''.join(l)  #list -> str      
isoall = [str(int(int(x)/10))+'.09c' for x in name]
del isoall[-1]
del isoall[-1]
goodiso = ['1001.09c', '1002.09c', '1003.09c', '2003.09c', '2004.09c', '3006.09c', '3007.09c', '4009.09c', '5010.09c', '5011.09c', '7014.09c', '7015.09c', '8016.09c', '8017.09c', '31069.09c', '31071.09c', '32070.09c', '32072.09c', '32073.09c', '32074.09c', '32076.09c', '33074.09c', '33075.09c', '34074.09c', '34076.09c', '34077.09c', '34078.09c', '34079.09c', '34080.09c', '34082.09c', '35079.09c', '35081.09c', '36078.09c', '36080.09c', '36082.09c', '36083.09c', '36084.09c', '36085.09c', '36086.09c', '37085.09c', '37086.09c', '37087.09c', '38084.09c', '38086.09c', '38087.09c', '38088.09c', '38089.09c', '38090.09c', '39089.09c', '39090.09c', '39091.09c', '40090.09c', '40091.09c', '40092.09c', '40093.09c', '40094.09c', '40095.09c', '40096.09c', '41093.09c', '41094.09c', '41095.09c', '42092.09c', '42094.09c', '42095.09c', '42096.09c', '42097.09c', '42098.09c', '42099.09c', '42100.09c', '43099.09c', '44098.09c', '44099.09c', '44100.09c', '44101.09c', '44102.09c', '44103.09c', '44104.09c', '44105.09c', '44106.09c', '45103.09c', '45105.09c', '46102.09c', '46104.09c', '46105.09c', '46106.09c', '46107.09c', '46108.09c', '46110.09c', '47107.09c', '47109.09c', '47310.09c', '47111.09c', '48106.09c', '48108.09c', '48110.09c', '48111.09c', '48112.09c', '48113.09c', '48114.09c', '48315.09c', '48116.09c', '49113.09c', '49115.09c', '50112.09c', '50113.09c', '50114.09c', '50115.09c', '50116.09c', '50117.09c', '50118.09c', '50119.09c', '50120.09c', '50122.09c', '50123.09c', '50124.09c', '50125.09c', '50126.09c', '51121.09c', '51123.09c', '51124.09c', '51125.09c', '51126.09c', '52120.09c', '52122.09c', '52123.09c', '52124.09c', '52125.09c', '52126.09c', '52327.09c', '52128.09c', '52329.09c', '52130.09c', '52132.09c', '53127.09c', '53129.09c', '53130.09c', '53131.09c', '53135.09c', '54126.09c', '54128.09c', '54129.09c', '54130.09c', '54131.09c', '54132.09c', '54133.09c', '54134.09c', '54135.09c', '54136.09c', '55133.09c', '55134.09c', '55135.09c', '55136.09c', '55137.09c', '56132.09c', '56133.09c', '56134.09c', '56135.09c', '56136.09c', '56137.09c', '56138.09c', '56140.09c', '57138.09c', '57139.09c', '57140.09c', '58138.09c', '58139.09c', '58140.09c', '58141.09c', '58142.09c', '58143.09c', '58144.09c', '59141.09c', '59142.09c', '59143.09c', '60142.09c', '60143.09c', '60144.09c', '60145.09c', '60146.09c', '60147.09c', '60148.09c', '60150.09c', '61147.09c', '61148.09c', '61348.09c', '61149.09c', '61151.09c', '62144.09c', '62147.09c', '62148.09c', '62149.09c', '62150.09c', '62151.09c', '62152.09c', '62153.09c', '62154.09c', '63151.09c', '63152.09c', '63153.09c', '63154.09c', '63155.09c', '63156.09c', '63157.09c', '64152.09c', '64153.09c', '64154.09c', '64155.09c', '64156.09c', '64157.09c', '64158.09c', '64160.09c', '65159.09c', '65160.09c', '66156.09c', '66158.09c', '66160.09c', '66161.09c', '66162.09c', '66163.09c', '66164.09c', '67165.09c', '67366.09c', '68162.09c', '68164.09c', '68166.09c', '68167.09c', '68168.09c', '68170.09c', '90227.09c', '90228.09c', '90229.09c', '90230.09c', '90232.09c', '90233.09c', '90234.09c', '91231.09c', '91232.09c', '91233.09c', '92232.09c', '92233.09c', '92234.09c', '92235.09c', '92236.09c', '92237.09c', '92238.09c', '92239.09c', '92240.09c', '92241.09c', '93235.09c', '93236.09c', '93237.09c', '93238.09c', '93239.09c', '94236.09c', '94237.09c', '94238.09c', '94239.09c', '94240.09c', '94241.09c', '94242.09c', '94243.09c', '94244.09c', '95241.09c', '95242.09c', '95342.09c', '95243.09c', '95244.09c', '95344.09c', '96240.09c', '96241.09c', '96242.09c', '96243.09c', '96244.09c', '96245.09c', '96246.09c', '96247.09c', '96248.09c', '96249.09c', '96250.09c', '29065.09c', '30065.09c', '30066.09c', '30067.09c', '30068.09c', '30070.09c', '44096.09c', '54124.09c', '56130.09c', '58136.09c', '69168.09c', '69169.09c', '69170.09c', '82206.09c', '82207.09c', '82208.09c', '83209.09c', '88223.09c', '88224.09c', '88225.09c', '88226.09c', '89225.09c', '89226.09c', '89227.09c', '90231.09c', '91229.09c', '91230.09c', '92230.09c', '92231.09c', '93234.09c', '94246.09c', '95240.09c', '97249.09c', '97250.09c', '98249.09c', '98250.09c', '98251.09c']
day = [2.8]

file = open(r"fuelmats","w")
comment  = '%--------------------------------------------------------------------------------------------------%'
file.write(comment + '\n' + '%-------- CANDU Fuel Material Input --------%\n' + comment + '\n\n')
for chan in range(len(channels)):
    #Refuel check
    if channels[chan] == refuel:
        #Direction check
        if direction == 'front':
            #Old bundles
            temp1 = dep.materials[channels[chan]+'1'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp2 = dep.materials[channels[chan]+'2'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp3 = dep.materials[channels[chan]+'11'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp4 = dep.materials[channels[chan]+'12'].getValues('days','adens',day,zai=dep.metadata['zai'])
            #Fresh bundles
            for ii in buns:
                file.write('mat '+ channels[chan] +str(ii) + ' sum vol 2144.404 burn 1\n')
                file.write(fresh)
                file.write('\n' + comment + '\n\n')
            #Shifted bundles
            file.write('mat '+ channels[chan] +'9' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp1[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            file.write('mat '+ channels[chan] +'10' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp2[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            
            #Old bundles
            file.write('mat '+ channels[chan] +'11' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp3[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            file.write('mat '+ channels[chan] +'12' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp4[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            
        #Direction check
        elif direction == 'back':
            #Old bundles
            temp1 = dep.materials[channels[chan]+'1'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp2 = dep.materials[channels[chan]+'2'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp3 = dep.materials[channels[chan]+'11'].getValues('days','adens',day,zai=dep.metadata['zai'])
            temp4 = dep.materials[channels[chan]+'12'].getValues('days','adens',day,zai=dep.metadata['zai'])
        
            #Old bundles
            file.write('mat '+ channels[chan] +'1' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp1[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            file.write('mat '+ channels[chan] +'2' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp2[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
        
            #Shifted bundles
            file.write('mat '+ channels[chan] +'3' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp3[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
            file.write('mat '+ channels[chan] +'4' + ' sum vol 2144.404 burn 1\n')
            iso = []
            adens = []
            for ii in range(len(isoall)):
                for jj in range(len(goodiso)):
                    if isoall[ii] == goodiso[jj]:
                        iso.append(isoall[ii])
                        adens.append(temp4[ii])
            for ii in range(len(iso)):
                file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
            file.write('\n' + comment + '\n\n')
        
            #fresh bundles
            for ii in buns:
                file.write('mat '+ channels[chan] +str(ii) + ' sum vol 2144.404 burn 1\n')
                file.write(fresh)
                file.write('\n' + comment + '\n\n')      
        continue        
    
    
    #Double refueling
    if second == True:
        if channels[chan] == ref2:
            #Direction check
            if direction2 == 'front':
                #Old bundles
                temp1 = dep.materials[channels[chan]+'1'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp2 = dep.materials[channels[chan]+'2'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp3 = dep.materials[channels[chan]+'11'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp4 = dep.materials[channels[chan]+'12'].getValues('days','adens',day,zai=dep.metadata['zai'])
                #Fresh bundles
                for ii in buns2:
                    file.write('mat '+ channels[chan] +str(ii) + ' sum vol 2144.404 burn 1\n')
                    file.write(fresh)
                    file.write('\n' + comment + '\n\n')
                #Shifted bundles
                file.write('mat '+ channels[chan] +'9' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp1[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                file.write('mat '+ channels[chan] +'10' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp2[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                
                #Old bundles
                file.write('mat '+ channels[chan] +'11' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp3[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                file.write('mat '+ channels[chan] +'12' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp4[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                
            #Direction check
            elif direction2 == 'back':
                #Old bundles
                temp1 = dep.materials[channels[chan]+'1'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp2 = dep.materials[channels[chan]+'2'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp3 = dep.materials[channels[chan]+'11'].getValues('days','adens',day,zai=dep.metadata['zai'])
                temp4 = dep.materials[channels[chan]+'12'].getValues('days','adens',day,zai=dep.metadata['zai'])
            
                #Old bundles
                file.write('mat '+ channels[chan] +'1' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp1[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                file.write('mat '+ channels[chan] +'2' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp2[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
            
                #Shifted bundles
                file.write('mat '+ channels[chan] +'3' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp3[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
                file.write('mat '+ channels[chan] +'4' + ' sum vol 2144.404 burn 1\n')
                iso = []
                adens = []
                for ii in range(len(isoall)):
                    for jj in range(len(goodiso)):
                        if isoall[ii] == goodiso[jj]:
                            iso.append(isoall[ii])
                            adens.append(temp4[ii])
                for ii in range(len(iso)):
                    file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
                file.write('\n' + comment + '\n\n')
            
                #fresh bundles
                for ii in buns2:
                    file.write('mat '+ channels[chan] +str(ii) + ' sum vol 2144.404 burn 1\n')
                    file.write(fresh)
                    file.write('\n' + comment + '\n\n')      
            continue
    
    for level in range(12):
        file.write('mat '+ channels[chan] +str(level+1) + ' sum vol 2144.404 burn 1\n')
        fuel = dep.materials[channels[chan]+str(level+1)]
        adensall = fuel.getValues('days','adens',day,zai=dep.metadata['zai'])
        iso = []
        adens = []
        for ii in range(len(isoall)):
            for jj in range(len(goodiso)):
                if isoall[ii] == goodiso[jj]:
                    iso.append(isoall[ii])
                    adens.append(adensall[ii])
        for ii in range(len(iso)):
            file.write(iso[ii] + ' ' + str(adens[ii][0]) + '\n')
        file.write('\n' + comment + '\n\n')
file.close()

if refdir == 'front':
	flip[indref1][indref2] = 'back'
if refdir == 'back':
	flip[indref1][indref2] = 'front'
	
ref.append([refchan,'FALSE',''])
	
f = open('history.csv','w', newline='')  
temp2 = csv.writer(f)
for row in ref:
    temp2.writerow(row)
f.close()

k = open('flip.csv','w', newline='')  
temp2 = csv.writer(k)
for row in flip:
    temp2.writerow(row)
k.close()