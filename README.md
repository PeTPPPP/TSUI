# Extracting TSUI

## Preparing environments
#### Create a python enviroment
```shell
    conda env -create -f enviroment.yml
    conda activate tsui
```
#### Install a chrome driver (For automated searching)

- Download and install Google Chrome at https://www.google.com/chrome/
- Open the Chrome browser, check the version at chrome://settings/help
- Download the corresponding version of ChromeDriver at https://chromedriver.chromium.org/downloads
- Copy the ChromeDriver (chromedriver) to the bin folder of the computer. (For Linux, please copy to /usr/local/bin/)


### Preparing input data
#### Download and copy JADER files
- Download 4 files of JADER from PMDA website:
- Copy the 4 files to resources/JADEROrigin
### Preparing authentication files 
- Create a Google could service json file with translation api and copy to
resource/Acc/google.json
- Obtain a Meddra account and save to resource/Acc/Meddra.txt (two lines, first line: account_id, second line: password)

## Running

#### Convert data to UTF-8

```shell
    python main.py -c
```
#### Extracting phrases
```shell
    python main.py -p
```
#### Online mapping phrases in KEGG and MEDDRA

```shell
    python main.py -a
```
#### Manually correction
```
    Manually create mapping file for drug names that does not
    appear on KEGG
    Input file:
    Output file: 
```
#### Translating 
```shell
    python main.py -t
```
#### Extracint TSUI dataset:
```shell
    python main.py -x
```