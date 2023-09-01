# TSUI

## Final datasets
#### Raw files
1) data/TSUI_ML.txt: In raw text for triples of drug-drug-side effect with the format of each line:
    ```
    Drug_name_1,Drug_name_2,Adverse_event,A,B,C,D,Ord,p-value
    ```
    Where [[a,b],[c,d]] is the values of the contingency table of Fisher's exact test, resulting in Ord and p-value

2) Bundle of reports in raw format
    resource/demo202104_utf_EN_final.txt, resource/drug202104_utf_EN_final.txt, resource/hist202104_utf_EN_final.txt, and
    resource/reac202104_utf_EN_final.txt

#### Filtered, numerically encoded files
Files can be found in the TSUI_reports.7z file due to size limitations. 
1) Machine learning dataset
   
   data/TSUI_Encoded/TSUI_ML_Encoded.txt: In numerical encoded format of TSUI_ML.txt:
    ```
    DrugID1,DrugID2,Adverse_eventID,A,B,C,D,Ord,p-value
    ```
    With the descriptions of the encoded values in two files: 1) data/TSUI_Encoded/ActiveIngredientList for DrugName and DrugId; 2) data/TSUI_Encoded/AdverseEventPreferredTermList for Adverse_event and Adverse_eventID


2) Pharmacovigilance reports
   
   data/TSUI_Encoded/DEMO, data/TSUI_Encoded/DRUG, data/TSUI_Encoded/HIST, data/TSUI_Encoded/REAC:
   Individual files correspond to resource/demo202104_utf_EN_final.txt, resource/drug202104_utf_EN_final.txt, resource/hist202104_utf_EN_final.txt, and resource/reac202104_utf_EN_final.txt, respectively, after correction for redundancy, character mismatches, etc. and conversion into a relational database format. NOTE: Due to these secondary steps, we encourage the use of this version of the dataset instead of the raw files. 
   


    The columns encoded by numerical values are:
    - reac202104_utf_EN_final.txt
      - AdverseEventPreferredTerm
      - Outcome
    - drug202104_utf_EN_final.txt
      - Involvement
      - Treatment
      - RiskCategorization
    - demo202104_utf_EN_final.txt
      - Sex
      - AgeBin
      - WeightBin
      - HeightBin
      - PatientSurveyStatus
      - ReportType
      - ReporterQualification

    The columns encoded by IDs:
    - hist202104_utf_EN_final.txt:
      - DiseaseID 
    - reac202104_utf_EN_final.txt:
      - AdverseEventPreferredTerm
    - drug202104_utf_EN_final.txt:
      - ActiveIngredient
      - ActiveIngredientFromProductName 
      - ReasonForUse

    The descriptions of the encoded values are in data/TSUI_Encoded/EncodedColumnValues with the format:
    ```
    Table name    Column Name    Coded Value    Description
    ```
    See data/TSUI_Encoded/ActiveIngredientList for DrugIDs and
    data/TSUI_Encoded/AdverseEventPreferredTermList for Adverse_eventIDs

## Code
### Preparing environments and input
#### Create a python enviroment
```shell
    conda env -create -f enviroment.yml
    conda activate tsui
```
#### Unzip data
```shell
   ./decomp.sh
```
#### Input descriptions
1) resource/JADERTransComb.txt:
  Contains merged information of each RecordId with English text.
  Format of each line (with tab seperator):
    ```
        RecordId drug1,drug2,...,drugn adverse_event1,adverse_event2,...,adverse_eventm
    ```
2) resource/demo202104_utf_EN_final.txt:
  Demographic information of patients in English with columns:
    ```
    PrimaryId	CaseId	Sex	AgeBin	WeightBin	HeightBin	ReportingDate	PatientSurveyStatus	ReportType	ReporterQualification	E2B
    ```
3) resource/drug202104_utf_EN_final.txt:
  Drug use information in English with columns:
    ```
    PrimaryId	CaseId	DrugNr	Involvement	ActiveIngredient	ActiveIngredientFromProductName	RouteOfAdministration	AdministrationStart	AdministrationEnd	Dosage	DosageUnit	MultipleDoses	ReasonForUse	Treatment	RecurrenceInformation	RiskCategorization
    ```
4) resource/hist202104_utf_EN_final.txt:
  History of diseases of patients in English with columns:
    ```
    PrimaryId	CaseId	DiseaseNr	DiseaseId
    ```
5) resource/reac202104_utf_EN_final.txt:
  Adverse events in English with columns:
    ```
    PrimaryId   CaseId  AdverseEventNr	AdverseEventPreferredTerm	Outcome DateOfOccurrence
    ```

### Running
#### Extracting TSUI for raw text format:
```shell
    python main.py -x
```

#### Encoding TSUI for numerical format:

```shell
    python main.py -e
```
