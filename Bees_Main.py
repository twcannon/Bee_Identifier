import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import os, csv, Image
import numpy as np 
from Bees_module import train_img_rgb_hist, individual, similarity_test, breed


#########################
#### Initializations ####
#########################

fig = plt.figure()   
#os.chdir("/Users/Thomas/Desktop/Code/Data_Science_Competition/Bees")
trainDir = '/home/ec2-user/Bees/images/train'
testDir = '/home/ec2-user/Bees/images/test'
num_pop = 8 ### num_pop/2 must be even
mutation_rate = 0.4
survive_percent = (1./2) 
num_generations = 20
weak_breed_chance = 0.8


#######################################
#### Training-Set Value Generation ####
#######################################
print 'Training-Set Value Generation'

hist_array_train,num_a,num_b = train_img_rgb_hist('train', trainDir,fig)
ratio = num_a/float((num_a+num_b)) #ratio of bombus/total
sqrt_total = np.sqrt(num_a+num_b)


########################################
#### Initial Similarity Calculation ####
########################################
print 'Initial Similarity Calculation'

hist_array = []
similarity_array = []
a_id_array = []
b_id_array = []
###### Loop over the initial population and create training data arrays ######
for i in range(0,num_pop): 
    hist_array_test,a_array,b_array = individual(ratio,testDir,fig)
    similarity = similarity_test(hist_array_train,hist_array_test)
    hist_array.append(hist_array_test)
    similarity_array.append(similarity)
    a_id_array.append(a_array)
    b_id_array.append(b_array)
    
    
    
######################################
#### First Generation Orientation ####
######################################
print 'First Generation Orientation'

children_a,children_b,parents_a,parents_b,sim_arr = breed(similarity_array, hist_array,a_id_array,b_id_array,survive_percent,weak_breed_chance)
new_gen_a = parents_a
new_gen_b = parents_b
for i in range(0,len(children_a)):
    new_gen_a.append(children_a[i])
    new_gen_b.append(children_b[i])



def mutate(mutation_rate,parents_a,parents_b):
    print 'Mutation'
    #for i in range(0,len(children_b)-1):
    #    for j in range(0,len(children_b[i])-1):
    #        rand = np.random.rand()
    #        if rand <= mutation_rate:
    #            rand_a = np.random.randint(0,len(children_a[i]))
    #            children_b[i][j],children_a[i][rand_a] = children_a[i][rand_a],children_b[i][j]
    #for i in range(0,len(parents_b)-1):
    #    for j in range(0,len(parents_b[i])-1):
    #        rand = np.random.rand()
    #        if rand <= mutation_rate:
    #            rand_a = np.random.randint(0,len(parents_a[i]))
    #            parents_b[i][j],parents_a[i][rand_a] = parents_a[i][rand_a],parents_b[i][j]
    #return children_a,children_b,parents_a,parents_b
    for i in range(0,len(parents_b)-1):
        for j in range(0,len(parents_b[i])-1):
            rand = np.random.rand()
            if rand <= mutation_rate:
                rand_a = np.random.randint(0,len(parents_a[i]))
                parents_b[i][j],parents_a[i][rand_a] = parents_a[i][rand_a],parents_b[i][j]
    return parents_a,parents_b






######  Reads in test data, converts to RGB, medians, and returns histogram data ######
def main_hist_test(num_pop,a_id_array,b_id_array,hist_array_train,sim_arr,testDir,mutation_rate):
    a_red = []
    a_green = []
    a_blue = []
    b_red = []
    b_green = []
    b_blue = []
    hist_array = []
    a_id_array,b_id_array = mutate(mutation_rate,a_id_array,b_id_array)
    for i in range(num_pop/2,len(a_id_array)):
        for j in range(0,len(a_id_array[i])):
            img = Image.open(testDir+'/'+a_id_array[i][j])
            red = np.array(img)[:,:,0]
            green = np.array(img)[:,:,1]
            blue = np.array(img)[:,:,2]
            a_red.append(red)
            a_green.append(green)
            a_blue.append(blue) 
        for j in range(0,len(b_id_array[i])):
            img = Image.open(testDir+'/'+b_id_array[i][j])
            red = np.array(img)[:,:,0]
            green = np.array(img)[:,:,1]
            blue = np.array(img)[:,:,2]
            b_red.append(red)
            b_green.append(green)
            b_blue.append(blue)         
        a_red_median = np.array(np.median(a_red, axis=0))
        a_green_median = np.array(np.median(a_green, axis=0))
        a_blue_median = np.array(np.median(a_blue, axis=0))
        b_red_median = np.array(np.median(b_red, axis=0))
        b_green_median = np.array(np.median(b_green, axis=0))
        b_blue_median = np.array(np.median(b_blue, axis=0))
        a_red_n, a_red_bins, a_red_patches = plt.hist(a_red_median.flatten(),bins=255)
        a_green_n, a_green_bins, a_green_patches = plt.hist(a_green_median.flatten(),bins=255)
        a_blue_n, a_blue_bins, a_blue_patches = plt.hist(a_blue_median.flatten(),bins=255)
        b_red_n, b_red_bins, b_red_patches = plt.hist(b_red_median.flatten(),bins=255)
        b_green_n, b_green_bins, b_green_patches = plt.hist(b_green_median.flatten(),bins=255)
        b_blue_n, b_blue_bins, b_blue_patches = plt.hist(b_blue_median.flatten(),bins=255)
        hist_array_single = a_red_n,a_green_n,a_blue_n,b_red_n,b_green_n,b_blue_n    
        similarity = similarity_test(hist_array_train,hist_array_single)
        hist_array.append(hist_array_single)
        sim_arr.append(similarity)    
    print sorted(sim_arr)
    return sim_arr











###################
#### Main Loop ####
###################
sim_trend = []
iteration = 1
for i in range(0,num_generations):
    print 'Generation Number '+str(iteration)
    iteration +=1
    a_id_array = new_gen_a
    b_id_array = new_gen_b
    similarity_array = main_hist_test(num_pop,a_id_array,b_id_array,hist_array_train,sim_arr,testDir,mutation_rate)
    sim_trend.append(sorted(similarity_array))
    children_a,children_b,parents_a,parents_b,sim_arr = breed(similarity_array, hist_array,a_id_array,b_id_array,survive_percent,weak_breed_chance)
    latest_ch_a,latest_ch_b,latest_pa_a,latest_pa_b = children_a,children_b,parents_a,parents_b
    #children_a,children_b,parents_a,parents_b = mutate(mutation_rate,children_a,children_b,parents_a,parents_b)
    new_gen_a = parents_a
    new_gen_b = parents_b
    for i in range(0,len(children_a)):
        new_gen_a.append(children_a[i])
        new_gen_b.append(children_b[i])
    print 'Writing CSV'
    with open('submission.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id','genus'])
        for i in range(0,len(latest_pa_a[0])):    
            spamwriter.writerow([latest_pa_a[0][i][:-4],'1'])
        for i in range(0,len(latest_pa_b[0])):    
            spamwriter.writerow([latest_pa_b[0][i][:-4],'0'])
plt4 = fig.add_subplot(313)
plt4.plot(sim_trend)


with open('similarity_trend.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(0,len(sim_trend)):
        spamwriter.writerow(sim_trend[i])

#plt.show()
print 'Done'

