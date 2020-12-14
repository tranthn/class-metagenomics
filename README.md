# Metagenomics Final - Phylogenetics Visualization
Course: 410.734

Name: Emily Tran [ttran66]

Date: 12/14/2020

## Project Goal
* This project is focused on visualizations for phylogenetic trees, going through the following steps:
    1. The setup and usage of a tool that takes in a metagenome sample and produces phylogenies in a structured output format
    2. Conversion of the output into a form usable by graphing/plotting libraries
    3. Scripts that can generate two types of graphs: denodrgrams and sunburst (hierarchy) plots

PhyloSift will be used to process a metagenomic sample and generate a phyloXML output to be converted. While there are several tools out there that do process phyloXML already ([archaeopteryx](http://www.phylosoft.org/archaeopteryx/) being one of the most popular chocies), these tend to be specialized phylogeny tools. I hope to convert more standard biological formats into something more generic that can be used by general purpose plotting or graphing libraries. The two main plotting libraries I will examine are Plotly and D3.js, linked below.

1. [Plotly](https://plotly.com/)
2. [D3.js](https://d3js.org/)

## 1: PhyloSift
* phylosift: https://figshare.com/articles/PhyloSift_markers_database/5755404
    - GitHub: https://github.com/gjospin/PhyloSift
    - PhyloSiftt API and usage documentation: https://phylosift.wordpress.com/tutorials/running-phylosift/phylosift-overview/
* *Note*: the URL cited in the GitHub link is outdated, while the figshare link is more recent and works as 12/2020

### Installation
1. the figshare archive will download as `5755404.zip`, which should be unziped and contains 4 zip archives within it:
    1. `phylosift_v1.0.1.tar.bz2`
    2. `markers_20140913.tgz` - older version of the target markers from the v1.0 of PhyloSift
    3. `markers.tgz` - this is the latest version of the markers from 2018, so this should be unpacked
    4. `ncbi.tgz`

1. copy and unzip files 1, 3, 4 from above into a directory which we will refer to as `<phylosift-root>`, so our file structure will look like:

        <phylosift-root>/
        |-- phylosift_v1.0.1/
        |   |--- bin/
        |   |--- phylosiftrc
        |   |--- PS_temp
        |   |   |--- <metagenome-filename-prefix>/
        |   |   |   |--- <metagenome-filename-prefix>.xml - this is where the phyloXML output which we can use is located
        |-- markers/
        |-- ncbi/

        You must run PhyloSift directly from its file location, rather than adding it to global $PATH

        The metagenome-file-name-prefix value is automatically based off the name of the input FASTA/FASTQ file passed into the PhyloSift run

1. navigate to `<phylosift-root>/phylosift_v1.0.1`
1. modify the configuration file `phylosiftrc`, lines 43 - 47:

        # modifying this ensures that PhyloSift will the local NCBI database and markers archive from step 2, rather than trying to load them over the web
        $marker_dir= "<phylosift-root>/markers";
        $markers_extended_dir="";
        $ncbi_dir = "<phylosift-root>/ncbi";
        $marker_base_url = "";
        $ncbi_url = "";

2. PhyloSift comes with sample data that can be used to test it, which takes about 30 minutes:
  
        # outputs to  <phylosift-root>/phylosift_v1.0.1/PS_temp/HMP_1.fastq.gz/
        # more details on files are at phylosift: https://phylosift.wordpress.com/tutorials/phylosift-outputs/
        cd <phylosift-root>/phylosift_v1.0.1
        ./phylosift all --paired tutorial_data/HMP_1.fastq.gz tutorial_data/HMP_2.fastq.gz

### sample metageome
* Metagenome: [sample fastq](https://portal.hmpdacc.org/files/596fc2de57601ec08a01fdee59e998a1)
   - ID: SRS104093
   - Download link: [http://downloads.hmpdacc.org/dacc/hhs/genome/microbiome/wgs/analysis/hmwgsqc/v2/SRS104093.tar.bz2]()
   - Subject: [HMP link](https://portal.hmpdacc.org/cases/596fc2de57601ec08a01fdee59087b8a)

---

## 2: Data Format Conversion 

* Python3 and its module manager *pip3* are required

### Python Dependency Installation

        pip3 install plotly
        pip3 install xmldtodict

        # ete3 and PyQt5 are used for calculating distance matrix when converting newick format to a format for Plotly denodrogram
        pip3 install PyQt5
        pip3 install ete3

### File Format Conversion

* phyloXML to Plotly format

        # -i: input file path
        # -o: file to store the intermediary data structure
        # -d: max traversal depth when converting the phyloXML structure, to help limit the tree depth/overall node count
        # -p: the target plot type, which determines the data structure output, options = [d3, plotly]
        ./convert_phylo_xml.py -i ../data/phylo-test.xml -o plotly.out -d 4 -p plotly

* phyloXML to JSON/D3-compatible format

        ./convert_phylo_xml.py -i ../data/phylo-test.xml -o test.json -d 4 -p d3
---

## 3: Graph Generation

* phyloXML Plotly output to Plotly sunburst graph:

        ./graph-phylo.py -i ../plotly.out

* Newick to Plotly denodrogram

        # -i: the input newick file
        ./graph-newick.py -i ../../data/newick-sample.txt