import glob,os
import trackhub
import pandas as pd
import numpy as np 
import sys



def defineHeight(new_name, dict_height):

    if dict_height.get(new_name) == 'ctl' or 'impute' in new_name:
        return '100:16:8' 

    else:
        return '100:32:8' #purple




# def defineColour(new_name, dict_colour):
#     """Receives a sample name including
#     the assay. Returns a string colour
#     according to the assay type."""

#     if dict_colour.get(new_name) == 'ctl':
#         return '0,0,139' #blue
   

#     if 'impute' in new_name:
#         return '0,100,0' #green

#     # if dict_colour.get(new_name) == 'e.e.c.a' or dict_colour.get(new_name) == 'e.e.c' and 'impute' not in new_name:
#     if dict_colour.get(new_name) == 'new':   
#         return '238,130,238'

#     else:
#         return '128,0,128' #purple



#Creating dict to rename samples
# df = pd.read_csv('scripts/names_trackhub.csv')
df = pd.read_csv('scripts/names_trackhub_final.csv')
#changing trackhub column
# to_rep = df['trackhub'].str.startswith('_')
# df['trackhub'] = np.where(to_rep,'new', df['trackhub'])

# print(df)
# sys.exit()

dict_names = dict(zip(df['md5sum'], df['final_name'])) #working
dict_color = dict(zip(df['md5sum'], df['color']))
dict_priority = dict(zip(df['final_name'], df['order'])) #get priority order
dict_height = dict(zip(df['final_name'], df['trackhub']))

# print(dict_color)
# sys.exit()



#creating hub
hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="EpiAtlas_potential_badQC",
    short_label='EpiAtlas_potential_badQC',
    long_label='EpiAtlas_potential_badQC',
    genome="hg38",
    email="frog2901@usherbrooke.ca")

# print(hub)


for bigwig in glob.glob('/home/frosig/scratch/EPILAP_IHEC/test/IMPUTED/trackhub_imputed_observed_badqc/data/*'):

    # track names can't have any spaces or special characters. Since we'll
    # be using filenames as names, and filenames have non-alphanumeric
    # characters, we use the sanitize() function to remove them.

    name=os.path.basename(bigwig)
    # if name in dict_names.keys():
    new_name = dict_names.get(name)
    color_track = dict_color.get(name)
    # print(new_name)
            
    # colour_track = defineColour(new_name, dict_colour) #colour function
    maxHeightPixels = defineHeight(new_name, dict_height) #maxHeightPixels function

    priority = dict_priority.get(new_name)

    #replacing specific symbols
    new_name = new_name.replace('.', '_')
    new_name = new_name.replace('+', '')
    # new_name = new_name.replace('-', '_')


    # new_name = trackhub.helpers.sanitize(new_name)
    # print(new_name, colour_track, priority)


    track = trackhub.Track(
    name=new_name,          # track names can't have any spaces or special chars.
    source=bigwig,      # filename to build this track from
    visibility='full',  # shows the full signal
    color=color_track,    # brick red
    autoScale='on', # allow the track to autoscale
    priority=priority,    
    maxHeightPixels=maxHeightPixels,
    tracktype='bigWig', # required when making a track
    )

    # print(track)
    # print('\n')
# Each track is added to the trackdb

    trackdb.add_tracks(track)

# print(trackdb)
trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='badQC_hub_add4')
