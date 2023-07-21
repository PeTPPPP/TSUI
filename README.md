# Extracting TSUI

## Preparing environments
#### Create a python enviroment
```shell
    conda env -create -f enviroment.yml
    conda activate tsui
```
### Required files
- data/JADERTransComb.txt

  Contain records with English translation.

  Format of each line (with tab seperator):
    ```

        RecordId drug1,drug2,...,drugn adverse_event1,adverse_event2,...,adverse_eventm
    
    ```
  (Because of the privacy,  only an example file is uploaded.)
#### Extracting TSUI dataset:
```shell
    python main.py -x
```

### Final dataset to download
```
    data/TSUI.txt
```
