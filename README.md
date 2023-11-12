# MidpointPlotter
This script makes fragment midpoint versus fragment lenght plots at specified genomic positions. Such plots are used in mNase-seq and ATAC-seq studies. See for example:
(https://www.pnas.org/doi/full/10.1073/pnas.1118898109)
(https://www.pnas.org/doi/abs/10.1073/pnas.1110731108)

**Motivation:** Pileup of sequenced reads is frequently used to visualize signal in genomics experiments however such representation looses information about the fragment length. Such information is important in the studies of the mechanisms of DNA protein binding. To address this need midpoint fragment plots were introduced in (https://www.pnas.org/doi/full/10.1073/pnas.1118898109). See image below for explanation.
<img src=./Images/pnas.1118898109fig03.jpeg>

**Usage MidpointPlotter**

Options:

       BAN file name
                sequences file name

       bed file name
                file with coordinates of genomic positions to visualize reads at; must contain coordinates and names of the position

       output file name
                name of the file with plots

       -w (optional) integer
                size of the window to plot; defaults to 150 bp

       -c (optional) True or False
                if True one plot for all genomic positions aggregated is produced; if set to FALSE one plot is produced for each position; defaults to True

       -f (optional) True or False
                if True saves to pdf file; if False saves to png file; defaults to False

       -h
                Show help message and exit

**To visualize fragment midpoints**

``python MidpointPlotter.py GSM836161_P20_20110726_8_sorted.bam centromers_yeast.bed cen_plots ``

Below is midpint plot of all budding yeast centromeres aggregated together. Sequence file is from (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM836161)
<img src=./Images/cen_plots.png> 
