import zipcodes
import csv
import random
from bulk_posting_format import bulk_format


ghost_headers = [
    "Origin City*",
    "Origin State*",
    "Origin Postal Code",
    "Destination City*",
    "Destination State*",
    "Destination Postal Code"
]

def ghost_post(origin_radius, destination_radius, quantity):
    origin_radius = int(origin_radius)
    destination_radius = int(destination_radius)
    quantity = int(quantity)
    with open("./bulk_posting.csv", newline='') as infile, open("./ghost_post.csv", "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=bulk_format)

        writer.writeheader()

        for row in reader:
            origin_zip = zipcodes.matching(row["Origin Postal Code"])[0]
            destination_zip = zipcodes.matching(row["Destination Postal Code"])[0]
            o_coords = (float(origin_zip["lat"]), float(origin_zip["long"]))
            d_coords = (float(destination_zip["lat"]), float(destination_zip["long"]))
            o_similar_zips = zipcodes.filter_by_coordinates(*o_coords, origin_radius)
            d_similar_zips = zipcodes.filter_by_coordinates(*d_coords, destination_radius)
            new_row = dict.fromkeys(bulk_format)
            for header in new_row:
                new_row[header] = row[header]
            for i in range(quantity):
                random_org_index = random.randrange(len(o_similar_zips))
                random_dest_index = random.randrange(len(d_similar_zips))
                ghost_org = o_similar_zips.pop(random_org_index)
                ghost_dest = d_similar_zips.pop(random_dest_index)
                new_row["Origin City*"] = ghost_org["city"]
                new_row["Origin State*"] = ghost_org["state"]
                new_row["Origin Postal Code"] = ghost_org["zip_code"]
                new_row["Destination City*"] = ghost_dest["city"]
                new_row["Destination State*"] = ghost_dest["state"]
                new_row["Destination Postal Code"] = ghost_dest["zip_code"]
                writer.writerow(new_row)
                '''writer.writerow({
                    "Origin City*" : ghost_org["city"],
                    "Origin State*" : ghost_org["state"],
                    "Origin Postal Code" : ghost_org["zip_code"],
                    "Destination City*" : ghost_dest["city"],
                    "Destination State*" : ghost_dest["state"],
                    "Destination Postal Code" : ghost_dest["zip_code"]
                })'''
            

#ghost_post("100")