# Disability Trends Dataset Instructions

This folder contains the various corpora used in the Disability Trends NLP project.

In order to avoid "bloating" the repo, the contents of this directory are ignored by Git, except for this README.

## Running the Project

If you want to run the project to explore it for yourself, there are two main ways this can be done: either by using the same dataset as for our project submitted for Spring 2024 CSCI 404, or by creating your own dataset.

> NOTE: Of course, the first step would be to clone the repo, but that will not be covered here.

### CSCI 404 Dataset

The dataset used in the course of this project for CSCI 404 can be downloaded from Google Drive [here](https://drive.google.com/drive/folders/14n1Ya01CuQU9YFKtIkQR06RBONfc9NNi?usp=sharing). Simply download it, and extract it to this location (so that the downloaded README overwrites this file).

### Using Your Own Data
Refer to the instructions in `/code/scrape/how_to/nexis_instructions.md` for information about how to download data from Nexis Uni (LexisNexis) (henceforth "Nexis"). Once you have done so, organize the data in this directory using the below structure for each key.

```
/code/data/
    | README.md (this file)
    | <key>
    |    | <decade1>
    |    |    | <rtfs1>
    |    |    |    | *.rtf
    |    |    |    | ...
    |    |    | <rtfs2>
    |    |    | ...
    |    |    | <rtfs#>
    |    |    | zips (optional)
    |    |    | json
    |    | <decade2>
    |    |    | <rtfs1>
    |    |    | <rtfs2>
    |    |    | ...
    |    |    | <rtfs#>
    |    |    | zips (optional)
    |    |    | json
    |    | ...
    |    | <decade#>
```

The names of each `<symbol>` are described below using informal [Backus–Naur Form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)

- **`<key> ::= <lowercase-letter>+`** *(e.g. `example`)* is a short and unique human-understandable identifier representing your search term or other means of separation.
- **`<decade> ::= <numeric>+ "s"`** *(e.g. `2020s`)* is used for sub-key data splitting. In the context of the original project, this was used for grouping documents by decade.
- **`<rtfs> ::= <decade> "-" <numeric> <first-of-key>`** *(e.g. `2020s-1e`, `2020s-2e`, etc. for `decade = "2020s"` and `key = "example"`)* is an extracted (and subsequently renamed) ZIP folder as downloaded from Nexis using the previously mentioned instructions.

Other directories are as described below.

- **`<key>/<decade>/zips`** is an <u>optional</u> folder containing the Nexis download zips themselves. This should only be included/used as a form of redundancy.
- **`<key>/<decade>/json`** is <u>automatically created</u> containing outputs from `rtf_scrape.py`, one .json file per `<rtfs>` directory, using the same name.