import matplotlib.pyplot as plt
import os, csv, random
import numpy as np 
import Image
import itertools

###### Sum of differences test for similarity ######
###### future inclusion: sum of diffferences / max ######
def similarity_test(train_array, test_array):
    sum_array = []
    for i in range(0,len(test_array)):
        #color_sum = sum(abs(train_array[0]-test_array[0]))
        sum_array.append(sum(abs(train_array[0]-test_array[0])))
    similarity = sum(sum_array)
    return similarity



###### Reads in training data, converts to RGB, medians, and returns histogram data ######
def train_img_rgb_hist(data, dataDir,fig):
    plt1 = fig.add_subplot(311)
    reader=csv.reader(open(data+"_labels.csv","rU"),delimiter=',')
    #x=list(reader)
    result=np.array(list(reader))
    result_matrix = result[range(1,len(result[:,0])),:]
    bee_id = result_matrix[:,0]                     
    bee_genus = result_matrix[:,1]      
    global type    
    a_red = []
    a_green = []
    a_blue = []
    b_red = []
    b_green = []
    b_blue = []
    #count = 1 
    for dirName, subdirList, fileList in os.walk(dataDir):
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            if fname.endswith(".jpg"):
                #count = count+1
                img = Image.open(dataDir+'/'+fname)
                red = np.array(img)[:,:,0]
                green = np.array(img)[:,:,1]
                blue = np.array(img)[:,:,2]      
                # tells us the species (type) of bee
                for j in range (0,len(bee_id)-1):
                    if bee_id[j] == fname[:-4]:
                        type = float(bee_genus[j])
            if type == 1: #bombus
                a_red.append(red)
                a_green.append(green)
                a_blue.append(blue)   
            if type == 0: #aphis
                b_red.append(red)
                b_green.append(green)
                b_blue.append(blue)           
            #if float(count) % 10 == 0:
                #print count            
    a_red_median = np.array(np.median(a_red, axis=0))
    a_green_median = np.array(np.median(a_green, axis=0))
    a_blue_median = np.array(np.median(a_blue, axis=0))
    b_red_median = np.array(np.median(b_red, axis=0))
    b_green_median = np.array(np.median(b_green, axis=0))
    b_blue_median = np.array(np.median(b_blue, axis=0))
    a_red_n, a_red_bins, a_red_patches = plt1.hist(a_red_median.flatten(),bins=255,range=(0,255), color='red',alpha=0.5)
    a_green_n, a_green_bins, a_green_patches = plt1.hist(a_green_median.flatten(),bins=255,range=(0,255), color='green',alpha=0.5)
    a_blue_n, a_blue_bins, a_blue_patches = plt1.hist(a_blue_median.flatten(),bins=255,range=(0,255), color='blue',alpha=0.5)
    b_red_n, b_red_bins, b_red_patches = plt1.hist(b_red_median.flatten(),bins=255,range=(0,255), color='magenta',alpha=0.5)
    b_green_n, b_green_bins, b_green_patches = plt1.hist(b_green_median.flatten(),bins=255,range=(0,255), color='yellow',alpha=0.5)
    b_blue_n, b_blue_bins, b_blue_patches = plt1.hist(b_blue_median.flatten(),bins=255,range=(0,255), color='cyan',alpha=0.5)
    num_a = np.array(a_red).shape
    num_b = np.array(b_red).shape
    hist_array = a_red_n,a_green_n,a_blue_n,b_red_n,b_green_n,b_blue_n
    return hist_array,num_a[0],num_b[0];    
    
    
    
    
######  Reads in test data, converts to RGB, medians, and returns histogram data ######
def individual(ratio,dataDir,fig):
    a_red = []
    a_green = []
    a_blue = []
    b_red = []
    b_green = []
    b_blue = []
    #count = 1
    #filecount = len(glob.glob1('/Users/Thomas/Desktop/Code/Data_Science_Competition/Bees/images/test_testing',"*.jpg"))
    for dirName, subdirList, fileList in os.walk(dataDir):
        #print('Found directory: %s' % dirName)
        a_array = []
        b_array = []
        for fname in fileList:
            if fname.endswith(".jpg"):
                #count = count+1
                img = Image.open(dataDir+'/'+fname)
                red = np.array(img)[:,:,0]
                green = np.array(img)[:,:,1]
                blue = np.array(img)[:,:,2]
            num = random.random()
            if num <= ratio:
                a_array.append(fname)
                a_red.append(red)
                a_green.append(green)
                a_blue.append(blue) 
            else:
                b_array.append(fname)
                b_red.append(red)
                b_green.append(green)
                b_blue.append(blue)       
            #if float(count) % 10 == 0:
            #    print count     
    a_red_median = np.array(np.median(a_red, axis=0))
    a_green_median = np.array(np.median(a_green, axis=0))
    a_blue_median = np.array(np.median(a_blue, axis=0))
    b_red_median = np.array(np.median(b_red, axis=0))
    b_green_median = np.array(np.median(b_green, axis=0))
    b_blue_median = np.array(np.median(b_blue, axis=0))
    #a_red_n, a_red_bins, a_red_patches = plt2.hist(a_red_median.flatten(),bins=255,range=(0,255), color='red',alpha=0.5)
    #a_green_n, a_green_bins, a_green_patches = plt2.hist(a_green_median.flatten(),bins=255,range=(0,255), color='green',alpha=0.5)
    #a_blue_n, a_blue_bins, a_blue_patches = plt2.hist(a_blue_median.flatten(),bins=255,range=(0,255), color='blue',alpha=0.5)
    #b_red_n, b_red_bins, b_red_patches = plt2.hist(b_red_median.flatten(),bins=255,range=(0,255), color='magenta',alpha=0.5)
    #b_green_n, b_green_bins, b_green_patches = plt2.hist(b_green_median.flatten(),bins=255,range=(0,255), color='yellow',alpha=0.5)
    #b_blue_n, b_blue_bins, b_blue_patches = plt2.hist(b_blue_median.flatten(),bins=255,range=(0,255), color='cyan',alpha=0.5)
    a_red_n, a_red_bins, a_red_patches = plt.hist(a_red_median.flatten(),bins=255)
    a_green_n, a_green_bins, a_green_patches = plt.hist(a_green_median.flatten(),bins=255)
    a_blue_n, a_blue_bins, a_blue_patches = plt.hist(a_blue_median.flatten(),bins=255)
    b_red_n, b_red_bins, b_red_patches = plt.hist(b_red_median.flatten(),bins=255)
    b_green_n, b_green_bins, b_green_patches = plt.hist(b_green_median.flatten(),bins=255)
    b_blue_n, b_blue_bins, b_blue_patches = plt.hist(b_blue_median.flatten(),bins=255)
    #num_a = np.array(a_red).shape
    #num_b = np.array(b_red).shape
    hist_array = a_red_n,a_green_n,a_blue_n,b_red_n,b_green_n,b_blue_n    
    return hist_array,a_array,b_array;




###### Breeds and swaps 'genes' in datasets ######
def gene_swap(male_index,female_index,fittest_a,fittest_b):
    #children = []
    children_a = []
    children_b = []
    for i in range(0,len(male_index)):
        ### Finds mutually exclusive and shared elements ###
        # mutually exclusive elements in male and female #
        mutex = np.setxor1d(fittest_a[male_index[i]],fittest_a[female_index[i]])
        np.random.shuffle(mutex) 
        # shared elements in male and female #
        # share[0] ~ a     share[1] ~ b #
        share = [np.intersect1d(fittest_a[male_index[i]],fittest_a[female_index[i]]),np.intersect1d(fittest_b[male_index[i]],fittest_b[female_index[i]])]  
        ### Determines lengths for setting up child ###
        if np.random.rand() >.5 == True:
            a_length = len(fittest_b[male_index[i]])
        else:
            a_length = len(fittest_b[female_index[i]])
        child_a = [mutex[:+int(a_length/2.)],share[0]]
        child_b = [mutex[+int(a_length/2.):],share[1]]
        child_a = list(itertools.chain(*child_a))
        child_b = list(itertools.chain(*child_b))
        #children.append(child)
        children_a.append(child_a)
        children_b.append(child_b)
    return children_a,children_b




###### Main control for breeding of data sets  ######
def breed(similarity_array, hist_array,a_id_array,b_id_array,survive_percent,weak_breed_chance):
    fittest_a = []
    fittest_b = []
    sim_arr = []
    rand_weak = np.random.randint((len(a_id_array)/2)-1,len(a_id_array))
    weak_sample_a = a_id_array[rand_weak]
    weak_sample_b = b_id_array[rand_weak]
    weak_sample_sim = similarity_array[rand_weak]
    for i in range(0,int(len(similarity_array)*survive_percent)):
        fittest_a.append(a_id_array[np.argmin(similarity_array)])
        fittest_b.append(b_id_array[np.argmin(similarity_array)])
        sim_arr.append(similarity_array[np.argmin(similarity_array)])
        del similarity_array[np.argmin(similarity_array)]
    if weak_breed_chance > np.random.rand():
        random_strong = np.random.randint((len(fittest_a)/2)-1,len(fittest_a))
        fittest_a[random_strong] = weak_sample_a
        fittest_b[random_strong] = weak_sample_b
        similarity_array[random_strong] = weak_sample_sim
    index_arr = np.arange(0,len(sim_arr))
    male_index = random.sample(index_arr,len(index_arr))
    female_index = male_index[-1:] + male_index[:-1]

    children_a,children_b = gene_swap(male_index,female_index,fittest_a,fittest_b)
    return children_a,children_b,fittest_a,fittest_b,sim_arr
