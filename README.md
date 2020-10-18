## Running Script

### Entrypoint
```sh
./parse-sam.py -input <file-name or directory with SAM files> -output <output directory>
```

* Example:

```sh
> ./parse-sam.py -input 1309.bowtie2.aligned.sam -output out
drawing graph for	1309.bowtie2.aligned.sam
saving graph to		out/1309.bowtie2.aligned.sam.graph.png
```

```sh
> ./parse-sam.py -input ./ -output out
processing file		./158.bowtie2.aligned.sam
drawing graph for	158.bowtie2.aligned.sam
saving graph to		out/158.bowtie2.aligned.sam.graph.png

processing file		./158.bwa.aligned.sam
drawing graph for	158.bwa.aligned.sam
saving graph to		out/158.bwa.aligned.sam.graph.png
...
```

### Extra Notes
* While the directory path version of the command will work, in practice, Python will eat up a lot of memory with the larger SAM files if it processes them in batch