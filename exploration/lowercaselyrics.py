import csv

with open('data-combined.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    rows = []

    for row in reader:
        # Lowercase the lyrics row
        row['Lyric'] = row['Lyric'].lower()

        rows.append(row)

with open('data-combined-lower.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)