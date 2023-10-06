# GeoMx Rename

Converts a fastq filename into the format needed by GeoMx NGS Pipeline

## About

From page 42 of the GeoMx NGS Readout User Manual: `The GeoMx NGS Pipeline looks for FASTQ files with 
a naming structure such as DSP-1001250001985-A-A02_S2_L001_R1_001.fastq.gz where DSP-1001250001985-A-A02 = Sample
ID matching Configuration file, SeqCodeIndices.csv, or Sample ID Translator File. S2 = Sample sheet
number. L001 = Lane number (include even if your flow cell had only 1 lane). R1 = Forward or reverse,
read 1 or 2. 001 = Should always be 001. The suffix .fastq.gz indicates a compressed file.`

This script takes a file with a filename formatting of `A02_CKDL230023209-1A_H75KCDSX7_L2_1.fq.gz` where `L2` is Lane number
and `1` is `R1` (forward read) and updates the filename to be `DSP-1001660018726-A-A02_S32_L002_R1_001.fastq.gz` where leading 
zeroes are added to the Lane number, `001` is added to the end of the filename, and `fastq` replaces `fq`. `Sample ID` and 
`Sample sheet number` are obtained from other necessary files (a configuration ini file and a QC or sample sheet to get the 
sample location).

## Installation

This has been run on Python 3.9 and 3.11.  Modules are os, gzip, argparse, and csv but should be included with the distro

## Usage

The script takes three arguments.  The first is the base sample name taken from the configuration ini file.  There should be a 
section that looks like:

`[AOI_List]
DSP-1001660018726-A-A01 = 1001660018726,A01,0.00
DSP-1001660018726-A-A02 = 1001660018726,A02,70025.09
DSP-1001660018726-A-A03 = 1001660018726,A03,159680.12
DSP-1001660018726-A-A04 = 1001660018726,A04,56077.51
DSP-1001660018726-A-A05 = 1001660018726,A05,55078.15
DSP-1001660018726-A-A06 = 1001660018726,A06,56267.45...`

`DSP-1001660018726-A-` is what would be used for the first argument

The second argument is a comma-separated or newline-delimited text file of the sample IDs `A01, A02, A03` (these correspond to 
the directory names).  The position in the text file should match the ordinal position on the sample sheet or QC file. These
may be in a file that looks like:

`Sample	(other columns deleted)
A08	
A12	
B02	
B03	
B04	
B05	
B06	
B07	
B09	
B10	
B11	
B12	
C01	
C02	`

So sample `A08` would be listed first, `A12` next, and so on.

The last argument is `--skip-gzip`.  For some reason the BaseSpace Sequence Hub can't read
the as-shipped gz files.  Normally decompressing and re-gzipping works but it adds a lot
of time.  If you've tested a few of the original files and BaseSpace doesn't complain
(usually it's an error on a bad separator) then the re-gzipping can be skipped.


## Development

Developed in Python 3.9

## Contributing

We welcome external contributions, although it is a good idea to contact the
maintainers before embarking on any significant development work to make sure
the proposed changes are a good fit.

Contributors agree to license their code under the license in use by this
project (see `LICENSE`).

To contribute:

  1. Fork the repo
  2. Make changes on a branch
  3. Create a pull request

## License

See `LICENSE` for details.

## Authors

**REPLACE:** Who should people contact with questions?

See `AUTHORS` the full list of authors.

