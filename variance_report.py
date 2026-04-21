import csv

# Materiality threshold: variances >= 10% are flagged as material

REPORT_FILE = 'May-August 2025 Financial Feasibility Report(python project).csv'

# decided to use utf-8-sig to remove the bytes at row[0] created by Excel
def read_csv(filename):
    data = []

    with open(filename ,encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            row['Budgeted Amount (ZMW)'] = float(row['Budgeted Amount (ZMW)'])
            row['Actual Amount (ZMW)'] = float(row['Actual Amount (ZMW)'])
            data.append(row)

    return data

# certain items were not budgeted for,the inf is used to address that and avoid ZeroDivisionError.
def calculate_variances(data):
    for row in data:
        row['Variance'] = row['Actual Amount (ZMW)'] - row['Budgeted Amount (ZMW)']
        if row['Budgeted Amount (ZMW)'] == 0:
            row['Variance %'] = float('inf')
        else:
            row['Variance %'] = round(((row['Variance'] / row['Budgeted Amount (ZMW)']) * 100),2)

# four-status model (including Unbudgeted) was used to account for items which were not budgeted for
def classify_status(data):
    for row in data:
        if row['Budgeted Amount (ZMW)'] == 0:
            row['Status'] = 'Unbudgeted'
        elif row['Actual Amount (ZMW)'] == row['Budgeted Amount (ZMW)']:
            row['Status'] = 'On Budget'
        elif row['Actual Amount (ZMW)'] > row['Budgeted Amount (ZMW)']:
            row['Status'] = 'Adverse'
        elif row['Actual Amount (ZMW)'] < row['Budgeted Amount (ZMW)']:
            row['Status'] = 'Favourable'

def flag_material(data,threshold):
    for row in data:
        if abs(row['Variance %']) >= threshold:
            row['Flag'] = '*'
        else:
            row['Flag'] = ''

# # weighted calculation: total variance over total budget.
# # Summing individual percentages would be mathematically meaningless because each row has a different base.

def calculate_totals(data):
    total_budgeted = sum(row['Budgeted Amount (ZMW)'] for row in data)
    total_actual = sum(row['Actual Amount (ZMW)'] for row in data)
    total_variance = total_actual - total_budgeted
    total_variance_pct = round((total_variance / total_budgeted) * 100,2)

    if total_actual == total_budgeted:
        overall_status = "On Budget"
    elif total_actual > total_budgeted:
        overall_status = "Adverse"
    else:
        overall_status = "Favourable"

    return {
        'total_budgeted': total_budgeted,
        'total_actual': total_actual,
        'total_variance': total_variance,
        'total_variance_pct': total_variance_pct,
        'overall_status': overall_status
    }

def count_material_flags(data):
    flagged_count  = len([row for row in data if row['Flag'] == '*'])
    total_count = len(data)

    return {
        'flagged_count': flagged_count,
        'total_count': total_count,
    }

def print_report(data, totals, counts, threshold):
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
    print(f"{counts['flagged_count']} of {counts['total_count']} categories have material variances (>{threshold}% threshold)")
    print(f"{'='*98}")

def main():

    filename = input(f'Enter the filename (default: {REPORT_FILE}): ') or REPORT_FILE
    while True:
        try:
            threshold = int(input('Enter threshold: '))
            break
        except ValueError:
            print('Please enter an integer')

    data = read_csv(filename)
    calculate_variances(data)
    classify_status(data)
    flag_material(data, threshold)
    counts = count_material_flags(data)
    totals = calculate_totals(data)
    print_report(data, totals, counts,threshold)

if __name__ == "__main__":
    main()
