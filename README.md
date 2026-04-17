###### \# Variance Report Generator

###### 

The script has four phases. First, it reads a CSV using csv.DictReader — I used utf-8-sig encoding because Excel adds a BOM to UTF-8 CSVs that breaks the first column key. Second, it calculates variance and variance percentage per row, handling zero-budget items with float('inf') to preserve numeric consistency instead of using a string like 'n/a'. Third, it classifies each row with a four-way status — Adverse, Favourable, On Budget, or Unbudgeted — and flags any row where the absolute variance percentage meets or exceeds 10%. Fourth, it computes totals using weighted variance percentage — total variance over total budget — because summing individual percentages across different bases is mathematically meaningless. Output is formatted using f-string width specifiers and aligned for readability. The script can be used by anyone from an individual tracking their expenses to businesses tracking projects.

---

###### 

###### \## Requirements

###### \- Python 3.x

###### \- No external dependencies

###### 

###### \## Input

###### \- CSV file with exact columns: Category, Budgeted Amount (ZMW), Actual Amount (ZMW)

###### \- One row per line item; no subtotals or totals

###### \- Example:

###### &#x20;   Category,Budgeted Amount (ZMW),Actual Amount (ZMW)

###### &#x20;   Potato Seed,1200,1200

###### &#x20;   Pesticide,200,220

###### 

###### \## How to Run

###### &#x20;   python variance\_report.py

###### 

###### \## Output


==================================================================================================
---

###### VARIANCE REPORT — Zamviazi Period 1 (Feb–May 2025)

###### ==================================================================================================

###### Category                                     Budget     Actual   Var(ZMW)    Var(%) Status    

###### \--------------------------------------------------------------------------------------------------

###### Buya Bamba Seed                               1,800      1,800          0       0.0% On Budget   

###### Nitrogen Fertiliser                           3,600      3,600          0       0.0% On Budget   

###### Folia Booster                                   600        600          0       0.0% On Budget   

###### Pesticide                                       600        660         60      10.0% Adverse    \*

###### Innoculant                                      600        600          0       0.0% On Budget   

###### Fungicide                                       600        660         60      10.0% Adverse    \*

###### Ploughing - Before Harvest                      600        800        200      33.3% Adverse    \*

###### Land Rent                                       500        500          0       0.0% On Budget   

###### Fuel                                          1,650      1,607        -43      -2.6% Favourable  

###### Transport Mazabuka - Chikankata (Person)        150        150          0       0.0% On Budget   

###### Transport Mazabuka - Chikankata (Load)          300        350         50      16.7% Adverse    \*

###### Miracle                                           0        460        460       inf% Unbudgeted \*

###### Transport Mazabuka (Load)                         0        125        125       inf% Unbudgeted





###### \## Key Decisions

###### \### BOM handling

###### i used utf-8-sig because excel adds a bom to utf-8 csv that breaks the first column key



###### \### Zero-budget items (float('inf'))

###### This was done in order to preserve numeric consistency across the script



###### \### Four-way status classification

###### This included the On budget, unbudgeted, favourable and adverse variances when variances were being calculated in order to account for all cases. From items without a budgeted amount, items where the budgeted and actual were the same, ones were the budgeted was greater than the actual and ones were the actual was greater than the budgeted.



###### \### Weighted variance percentage

###### total variance over total budget — because summing individual percentages across different bases is mathematically meaningless



###### \### Material threshold (10%)

###### Used to flag any variances that meet or exceed the threshold



###### \## Known Limitations

###### \- Hardcoded input filename (see stretch goals)

###### \- no error handling

###### 

###### \## Author

###### Kunda Ng'ambi

###### 

###### \## Version History

###### \- 0.1 — Initial working version: CSV ingestion, variance calculation, formatted output

