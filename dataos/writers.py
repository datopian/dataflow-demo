import csv

def csvwriter(resource):
    writer = csv.writer(open(resource.path, 'w'))
    writer.writerow(resource.headers)
    for row in resource.rows():
        writer.writerow(row)

