import csv

# Materiality threshold: variances >= 10% are flagged as material
THRESHOLD = 10

REPORT_FILE  = 'May-August 2025 Financial Feasibility Report(python project).csv'
data = []

# decided to use utf-8-sig to remove the bytes at row[0] created by excel
with open(REPORT_FILE ,encoding='utf-8-sig', newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        row['Budgeted Amount (ZMW)'] = float(row['Budgeted Amount (ZMW)'])
        row['Actual Amount (ZMW)'] = float(row['Actual Amount (ZMW)'])
        data.append(row)

# certain items where not budgeted for,the inf is used to address that and avoid ZeroDivisionError.
for row in data:
    row['Variance'] = row['Actual Amount (ZMW)'] - row['Budgeted Amount (ZMW)']
    if row['Budgeted Amount (ZMW)'] == 0:
        row['Variance %'] = float('inf')
    else:
        row['Variance %'] = round(((row['Variance'] / row['Budgeted Amount (ZMW)']) * 100),2)

# four-status model (including Unbudgeted) was used to account for items which were not budgeted for
for row in data:
    if row['Budgeted Amount (ZMW)'] == 0:
        row['Status'] = 'Unbudgeted'
    elif row['Actual Amount (ZMW)'] == row['Budgeted Amount (ZMW)']:
        row['Status'] = 'On Budget'
    elif row['Actual Amount (ZMW)'] > row['Budgeted Amount (ZMW)']:
        row['Status'] = 'Adverse'
    elif row['Actual Amount (ZMW)'] < row['Budgeted Amount (ZMW)']:
        row['Status'] = 'Favourable'



for row in data:
    if abs(row['Variance %']) >= THRESHOLD:
        row['Flag'] = '*'
    else:
        row['Flag'] = ''

# weighted calculation: total variance over total budget.
# Summing individual percentages would be mathematically meaningless because each row has a different base.
total_budgeted = sum(row['Budgeted Amount (ZMW)'] for row in data)
total_actual = sum(row['Actual Amount (ZMW)'] for row in data)
total_variance = total_actual - total_budgeted
total_variance_pct = round((total_variance / total_budgeted) * 100,2)
overall_status = ""

if total_actual == total_budgeted:
    overall_status = "On Budget"
elif total_actual > total_budgeted:
    overall_status = "Adverse"
else:
    overall_status = "Favourable"

totals = {
    'total_budgeted': total_budgeted,
    'total_actual': total_actual,
    'total_variance': total_variance,
    'total_variance_pct': total_variance_pct,
    'overall_status': overall_status
}


flagged_count  = len([row for row in data if row['Flag'] == '*'])
total_count = len(data)

print(f"\n{'='*98}")
print('VARIANCE REPORT — Zamviazi Period 1 (Feb–May 2025)')
print(f"{'='*98}")

print(f"{'Category':<40} {'Budget':>10} {'Actual':>10} {'Var(ZMW)':>10} {'Var(%)':>9} {'Status':<10}")

print(f"{'-'*98}")
for row in data:
    print(f"{row['Category']:<40} {row['Budgeted Amount (ZMW)']:>10,.0f} {row['Actual Amount (ZMW)']:>10,.0f} {row['Variance']:>10,.0f} {row['Variance %']:>9,.1f}% {row['Status']:<10} {row['Flag']:<1}")

print(f"{'-'*98}")

print(f"{'TOTALS':<40} {totals['total_budgeted']:>10,.0f} {totals['total_actual']:>10,.0f} {totals['total_variance']:>10,.0f} {totals['total_variance_pct']:>9,.1f}% {totals['overall_status']:<10}")

print(f"{'='*98}")
print(f'{flagged_count} of {total_count} categories have material variances (>{THRESHOLD}% threshold)')
print(f"{'='*98}")


