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



###### ```

###### &#x20;   Category,Budgeted Amount (ZMW),Actual Amount (ZMW)

###### &#x20;   Potato Seed,1200,1200

###### &#x20;   Pesticide,200,220

###### ```

###### 

###### \## How to Run

###### &#x20;   python variance\_report.py

###### 

###### \## Output

###### 

###### ```

###### ==================================================================================================

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

###### Transport Mazabuka (Load)                         0        125        125       inf% Unbudgeted \*

###### Transport Chikankata (Load)                       0        125        125       inf% Unbudgeted \*

###### Empty Bags                                       90         90          0       0.0% On Budget   

###### Transport Chikankata - Mazabuka (Person)        150        150          0       0.0% On Budget   

###### Transport Chikankata - Mazabuka (Load)        1,350      1,350          0       0.0% On Budget   

###### Ploughing - During Harvest                      200        200          0       0.0% On Budget   

###### Labour - During Harvest                         200        200          0       0.0% On Budget   

###### Council Levy                                    100        100          0       0.0% On Budget   

###### Deport Fees                                     300        300          0       0.0% On Budget   

###### Extra Hand Labourer                             500        500          0       0.0% On Budget   

###### Food - During Sales                             200        250         50      25.0% Adverse    \*

###### Transaction Charges - Bank                       30         30          0       0.0% On Budget   

###### Transaction Charges - Withdraw                   55         55          0       0.0% On Budget   

###### \--------------------------------------------------------------------------------------------------

###### TOTALS                                       14,175     15,262      1,087       7.7% Adverse   

###### ==================================================================================================

###### 8 of 25 categories have material variances (>10% threshold)

###### ==================================================================================================

```

---



###### \## Key Decisions

###### \### BOM handling

###### I used UTF-8-sig because Excel adds a BOM to UTF-8 CSV that breaks the first column key.



###### \### Zero-budget items (float('inf'))

###### When an item has zero budget but non-zero actual spend, the percentage variance is mathematically undefined (division by zero). Storing float('inf') preserves the numeric type of the column so downstream operations don't break on mixed string/number data. These rows are flagged as 'Unbudgeted' in the Status column for clarity.



###### \### Four-way status classification

###### Covers four scenarios: items with no budget (Unbudgeted), items where actual equals budget (On Budget), items where actual is less than budget (Favourable), and items where actual exceeds budget (Adverse).

###### 

###### \### Weighted variance percentage

###### Total variance over total budget. Summing individual percentages across different bases would be mathematically meaningless — a 10% variance on a 3,600 ZMW item is not equivalent to a 10% variance on a 30 ZMW item.

###### 

###### \### Material threshold (10%)

###### The threshold is currently hardcoded as 10 but designed as a constant (THRESHOLD) so it can be changed in one place. It's an absolute-value comparison, so both 15% over-budget and 15% under-budget trigger the flag.



###### \## Known Limitations

* ###### No command-line arguments (filename and threshold are hardcoded).
* ###### No output-to-file capability yet (report prints to terminal only).
* ###### No multi-period comparison.



###### \## Author

###### Kunda Ng'ambi

###### 

###### \## Version History

###### \- 0.1 — Initial working version: CSV ingestion, variance calculation, formatted output

