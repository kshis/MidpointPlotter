import argparse
import os
import pysam
import pandas as pd
import plotnine
from plotnine import *
import warnings
import sys, getopt

##################################################################################
####Command line arguments
####
####
parser = argparse.ArgumentParser(
                    prog='MidpointPlotter.py',
                    description='Plots reads midpoint.',
                    epilog='')

parser.add_argument('bamfile_name')
parser.add_argument('points_file_name')
parser.add_argument('output_file_name')
parser.add_argument('-w', '--window_to_plot',default=150)      
parser.add_argument('-c', '--combine',default = "True", choices=["True","true","False","false"])      
parser.add_argument('-f', '--pdf_format',default = "False", choices=["True","true","False","false"])  

args = parser.parse_args()
print(args.bamfile_name, args.points_file_name, args.output_file_name,args.window_to_plot,args.combine,args.pdf_format)

bamfile_name = args.bamfile_name
points_file_name = args.points_file_name
output_file_name = args.output_file_name

if args.combine == "True" or args.combine == "true":
	combine = True
else:
	combine = False
window_to_plot = args.window_to_plot

if args.pdf_format == "True" or args.pdf_format == "true":
	pdf = True
else:
	pdf = False

print(combine)
print(pdf)
def DrawMidpointPlot(dataframe_to_plot, window_to_plot, title_to_plot):
    return ggplot(dataframe_to_plot, aes(x='midpoint', y='length')) + geom_point(size=0.01,color="green") + xlim(-(window_to_plot), (window_to_plot)) + geom_vline(xintercept = 0)+labs(title = title_to_plot,
            x ="Distance from center, bp", y = "fragment size, bp")

##################################################################################
#### Read in data
####
try:
    print("Reading bam file.")
    bamfile = pysam.AlignmentFile(bamfile_name, "rb")
except:
    print("Error reading sequence file")
    raise
try:
    print("Reading interval file.")
    df_points = pd.read_table(points_file_name,header=None)
except:
    print("Error reading intervals file")
    raise

##################################################################################
#### Some input validation
####
if len(df_points) < 1:
    print("No intervals provided. Exiting.")
    raise
if df_points.shape[1] < 4:
    print("Not enough interval information. Please provide location and name for each interval. Exiting.")
    raise Exception("Bad interval input.")

##################################################################################
list_of_plots = []
all_my_fragments = []
all_fragment_length = []
all_fragment_midpoint = []

for i in range(len(df_points)):
    fragment_midpoint = []
    fragment_length = []

    center = df_points.iloc[i, 1]+(df_points.iloc[i, 2]-df_points.iloc[i, 1])/2
    print(center)
    iter = bamfile.fetch(df_points.iloc[i, 0],center-10000,center+10000)

    for x in iter:
        fragment_length.append(x.tlen)
        fragment_midpoint.append(((x.reference_start+x.tlen/2)-center))
    
    if combine == True:
        all_fragment_length.extend(fragment_length)
        all_fragment_midpoint.extend(fragment_midpoint)

    if combine == False:
        my_fragments = pd.DataFrame()
        my_fragments['midpoint']  = fragment_midpoint
        my_fragments['length']  = fragment_length
        list_of_plots.append(DrawMidpointPlot(my_fragments,window_to_plot,df_points.iloc[i, 3]))

if combine == True:
    all_my_fragments_df = pd.DataFrame()
    all_my_fragments_df['midpoint']  = all_fragment_midpoint
    all_my_fragments_df['length']  = all_fragment_length
    list_of_plots.append(DrawMidpointPlot(all_my_fragments_df,window_to_plot,"Combined intervals"))

##############################################################################
#######   Save plots
##############################################################################
warnings.filterwarnings("ignore")

if pdf == True:
    save_as_pdf_pages(list_of_plots,output_file_name+".pdf")
else:
    for i in range(len(list_of_plots)):
        if(len(list_of_plots) > 1):
            list_of_plots[i].save(output_file_name+"_"+str(i)+".png")
        else:
            list_of_plots[i].save(output_file_name+".png")
