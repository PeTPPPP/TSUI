# Extracting TSUI

## Preparing environments
#### Create a python enviroment
```shell
    conda env -create -f enviroment.yml
    conda activate tsui
```
#### Unzip data
```shell
   ./decomp.sh
```
### Input descriptions
- resource/JADERTransComb.txt:

  Contain merged information of each RecordId with English text.
  Format of each line (with tab seperator):
    ```

        RecordId drug1,drug2,...,drugn adverse_event1,adverse_event2,...,adverse_eventm
    
    ```
- resource/demo202104_utf_EN_final.txt:

  Demographic information of patients in English text with the columns:
    ```
    PrimaryId	CaseId	Sex	AgeBin	WeightBin	HeightBin	ReportingDate	PatientSurveyStatus	ReportType	ReporterQualification	E2B
    ```
- resource/drug202104_utf_EN_final.txt:

  Drug usage information in English text with the columns:

    ```
    PrimaryId	CaseId	DrugNr	Involvement	ActiveIngredient	ActiveIngredientFromProductName	RouteOfAdministration	AdministrationStart	AdministrationEnd	Dosage	DosageUnit	MultipleDoses	ReasonForUse	Treatment	RecurrenceInformation	RiskCategorization
    ```
- resource/hist202104_utf_EN_final.txt:

  History of diseases of patients in English text with the columns:
    ```
    PrimaryId	CaseId	DiseaseNr	DiseaseId
    ```
- resource/reac202104_utf_EN_final.txt:

  Adverse events in English text with the columns:
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

### Final dataset
- data/TSUI_ML.txt: In raw text for triples of drug-drug-side effect with the format of each line:
```
Drug_name_1,Drug_name_2,Adverse_event,A,B,C,D,Ord,p-value

```
    
   Where [[a,b],[c,d]] is the values of the contingency table of Fisher's exact test, resulting in Ord and p-value

  
- data/TSUI_Encoded/TSUI_ML_Encoded.txt: In numerical encoded format of TSUI_ML.txt:
```
DrugID1,DrugID2,Adverse_eventID,A,B,C,D,Ord,p-value

```
With the descriptions of the encoded values in two files:
data/TSUI_Encoded/ActiveIngredientList for DrugName\tDrugId and data/TSUI_Encoded/AdverseEventPreferredTermList for Adverse_event\tAdverse_eventID

- data/TSUI_Encoded/DEMO, data/TSUI_Encoded/DRUG, data/TSUI_Encoded/HIST, data/TSUI_Encoded/REAC:
Numerical encoded files of resource/demo202104_utf_EN_final.txt, resource/drug202104_utf_EN_final.txt, resource/hist202104_utf_EN_final.txt, and
resource/reac202104_utf_EN_final.txt, respectively. The columns to encode by numerical values are as follows:
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
    The columns to encode in seperated files:
    - hist202104_utf_EN_final.txt:
        - DiseaseID 
    - reac202104_utf_EN_final.txt:
        - AdverseEventPreferredTerm
    - drug202104_utf_EN_final.txt:
        - ActiveIngredient
        - ActiveIngredientFromProductName 
        - ReasonForUse

  - The descriptions of the encoded values are in data/TSUI_Encoded/EncodedColumnValues with the format:
  Table name\tColumn Name\tCoded Value\tDescription, and data/TSUI_Encoded/ActiveIngredientList for DrugID and data/TSUI_Encoded/AdverseEventPreferredTermList for Adverse_eventID
