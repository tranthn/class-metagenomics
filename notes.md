# project proposal ideas
date: 11/29/2020

## visualize interface / visualization ideas
### metagenome -> phylogenetic analysis -> graph pipeline
* would need good documentation and example input data (shortened if needed) as if this were to be published to github for general usage, per professor

### tools
* phylosift: https://figshare.com/articles/PhyloSift_markers_database/5755404
    - github: https://github.com/gjospin/PhyloSift
    - phylosift documentation: https://phylosift.wordpress.com/tutorials/running-phylosift/phylosift-overview/
* unzip the figshare archive (which contains 4 zipped archives within it) to something we'lll call phylosift-root
* must run phylosift from its directory location rather than adding it to global $PATH
* modify phylosiftrc, lines 43 - 47:

        $marker_dir= "<phylosift-root>/markers";
        $markers_extended_dir="";
        $ncbi_dir = "<phylosift-root>/ncbi";
        $marker_base_url = "";
        $ncbi_url = "";

* sample run (took about 30 minutes):
  
        cd <phylosift-root>/phylosift_v1.0.1
        ./phylosift all --paired tutorial_data/HMP_1.fastq.gz tutorial_data/HMP_2.fastq.gz

        # outputs to PS_temp/HMP_1.fastq.gz/
        # more details on files are at phylosift: https://phylosift.wordpress.com/tutorials/phylosift-outputs/
        # krona uses sequence_taxa.txt or sequence_taxa_summary.txt for visualization, it seems

#### phylosift data output
* default *.html graph *seems to* use the row items that are `concat` markers only
* snippet from `sequence_taxa_summary.txt`, manually re-sorted:
  
        Sequence_ID	                           Hit_Coordinates	NCBI_Taxon_ID Taxon_Rank	    Taxon_Name	Cumulative_Probability_Mass	    Markers_Hit
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	1	        no rank	        ROOT	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	1	        no rank	        ROOT	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	131567	    no rank	        CELLULAR ORGANISMS	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	131567	    no rank	        CELLULAR ORGANISMS	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	2	        superkingdom	BACTERIA	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	2	        superkingdom	BACTERIA	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	1239	    phylum	        FIRMICUTES	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	1239	    phylum	        FIRMICUTES	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	186801	    class	        CLOSTRIDIA	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	186801	    class	        CLOSTRIDIA	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	186802	    order	        CLOSTRIDIALES	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	186802	    order	        CLOSTRIDIALES	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	541000	    family	        RUMINOCOCCACEAE	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	541000	    family	        RUMINOCOCCACEAE	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	292632	    genus	        SUBDOLIGRANULUM	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	292632	    genus	        SUBDOLIGRANULUM	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	214851	    species	        SUBDOLIGRANULUM VARIABILE	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	214851	    species	        SUBDOLIGRANULUM VARIABILE	1	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	1.99	411471	    no rank	        SUBDOLIGRANULUM VARIABILE DSM 15176	0.5	concat
        SRR041662.11238925 HWUSI-EAS776_61BNN:5:69:732:1320	3.98	411471	    no rank	        SUBDOLIGRANULUM VARIABILE DSM 15176	0.5	concat

* this chunk is only for 1 sequence ID, with the rows sorted by taxon rank (from root/cellular -> species/no rank leaf)
* for the above, the SUBDOLIGRANULUM VARIABILE DSM 15176 is the leaf node
* unclear how the logic differentiates betweeen no rank for root/organisms and the leaf node SUBDOLIGRANULUM VARIABILE DSM 15176
* SUBDOLIGRANULUM VARIABILE DSM 15176 seemingly comprises 2% of total graph and 50% of SUBDOLIGRANULUM VARIABILE

* another snippet:

        Sequence_ID	                           Hit_Coordinates	NCBI_Taxon_ID	Taxon_Rank	Taxon_Name	Cumulative_Probability_Mass 	Markers_Hit
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	1	        no rank	        ROOT	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	131567      no rank	        CELLULAR ORGANISMS	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	2	        superkingdom	BACTERIA	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	68336       superphylum	        BACTEROIDETES/CHLOROBI GROUP	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	976	        phylum	        BACTEROIDETES	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	171549      order	        BACTEROIDALES	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	200643      class	        BACTEROIDIA	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	171552      family	        PREVOTELLACEAE	0.64945979602372	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	838	        genus	        PREVOTELLA	0.64945979602372	concat

        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	310514      species	        PREVOTELLA MULTISACCHARIVORAX	0.419225239788335	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	52227       species	        PREVOTELLA DENTALIS	0.0404329724861323	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	282402      species	        PREVOTELLA MULTIFORMIS	0.036292522389329	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	242750      species	        PREVOTELLA BERGENSIS	0.0233774227420187	concat

        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	688246      no rank	        PREVOTELLA MULTISACCHARIVORAX DSM 17128	0.209612619894168	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	908937      no rank	        PREVOTELLA DENTALIS DSM 3688	0.0202164862430662	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	888743      no rank	        PREVOTELLA MULTIFORMIS DSM 16608	0.0181462611946645	concat
        SRR041662.12249849 HWUSI-EAS776_61BNN:5:75:685:197	2.94	585502      no rank	        PREVOTELLA BERGENSIS DSM 17361	0.0116887113710094	concat

* note how there are multiple species options on the same coordinates, but PREVOTELLA MULTISACCHARIVORAX has highest probability with 0.41 and is the only one graphed
* also seems to pick higher ranked genuses too (see PARABACTEROIDES DISTASONIS vs. PARABACTEROIDES MERDAE, where only latter species is graphed)

### sample data
* Metagenome: [sample *.fastq](https://portal.hmpdacc.org/files/596fc2de57601ec08a01fdee59e998a1)
   - ID: SRS104093
   - Download link: [http://downloads.hmpdacc.org/dacc/hhs/genome/microbiome/wgs/analysis/hmwgsqc/v2/SRS104093.tar.bz2]()
   - Subject: [HMP link](https://portal.hmpdacc.org/cases/596fc2de57601ec08a01fdee59087b8a)
* sample GFF3 file: https://portal.hmpdacc.org/files/c3da055b4f1c6b91a79d82ec2e3cb889
* random fasta (from gingiva): https://portal.hmpdacc.org/files/54a24ca84a57a7d5b06687939f620d69

---

## dependencies
* https://github.com/martinblech/xmltodict        

        pip3 install scipy - nvm
        pip3 install plotly
        pip3 install xmldtodic