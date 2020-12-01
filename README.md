# Midterm

## Running Script

### Script Entrypoint
```sh
./parse-sam.py -input <file-name or directory with SAM files> -output <output directory>
```

#### Example

```sh
> ./parse-sam.py -input 1309.bowtie2.aligned.sam -output out
drawing graph for	1309.bowtie2.aligned.sam
saving graph to		out/1309.bowtie2.aligned.sam.graph.png
```

```sh
> ./parse-sam.py -input ../data/aligned -output frps
processing file		../data/aligned/837.bowtie2.aligned.sam
drawing graph for	837.bowtie2.aligned.sam
saving graph to		frps/837.bowtie2.aligned.sam.graph.png

processing file		../data/aligned/28132.bowtie2.bridged.aligned.sam
drawing graph for	28132.bowtie2.bridged.aligned.sam
saving graph to		frps/28132.bowtie2.bridged.aligned.sam.graph.png
...
```

---

### Name Mappings JSON
* Used to map organism name, taxon ID, and accession for usage in graph title

#### Example

```json
{
    "id": "NC_013520.1",
    "taxon": 29466,
    "name": "Veillonella parvula"
}
```

---

### Extra Notes
* While the directory path version of the command will work, in practice, Python will eat up a lot of memory with the larger SAM files if it processes them in batch
* I'd suggest processing the very large files (> 1GB) individually and calculate the remainder in batch