#VASSAR URSI 2020 Cross Registration PARAMETERS

#Path that contains the minian folder
minian_path = "."

dpath = "./videos/ENTER/PATH/HERE"

#Specify the file information. f_pattern is a regular expression identifying
#the naming pattern of minian output folders with a regex expression
#(e.g. 'minian$', or r'minian\.[0-9]+$' if data is batch processed and has a
#timestamp), and id_dims should be a list containing metadata identifiers used
#when analyzing the individual sessions (e.g. ['session','animal']).
f_pattern = 'pipeline_output$'
id_dims = ['session']

#Determines the parameters for cross registration. param_t_dist defines the
#maximal distance between cell centroids (in pixel units) on different sessions
#to consider them as the same cell
param_t_dist = 5
output_size = 90
