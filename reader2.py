import pandas as pd
import csv
import sys

def template_write(filepath):
    with open(filepath, newline='') as f:
        reader = pd.read_csv(f)
        reader = reader.sort_values('Origin_City')
        reader = reader.reset_index(drop=True)
        #print(reader)
        final_templates = ""
        with open("daily_templates.txt", "w") as templates:
            for index, row in reader.iterrows():
                origin_city = reader.loc[index, "Origin_City"]
                origin_state = reader.loc[index, "Origin_State"]
                origin_zip = reader.loc[index, "Origin_Zip"]
                destination_city = reader.loc[index, "Destination_City"]
                destination_state = reader.loc[index, "Destination_State"]
                destination_zip = reader.loc[index, "Destination_Zip"]
                carrier_miles = reader.loc[index, "Carrier_Miles"]
                trailer_length = reader.loc[index, "Trailer_Length"]
                equipment = reader.loc[index, "Equipment"]
                special_notes = reader.loc[index, "Special_Instructions_and_Rate_Confirmation_Notes"]
                revenue = reader.loc[index, "Revenue"]
                ready_date = reader.loc[index, "Ready_Date"]
                ship_by = reader.loc[index, "Ship_By_Date"]
                internal_notes = reader.loc[index, "Internal_Notes"]
                receiver_appointment = reader.loc[index, "Receiver_Appointment_Datetime"]
                del_avail = reader.loc[index, "Del_Avail_Date"]
                must_del = reader.loc[index, "Must_Del_Date"]
                weight = reader.loc[index, "Weight"]
                beginning_buy = reader.loc[index, "Beginning_Buy_Rate"]

                if (
                    index != 0 and 
                    origin_city == reader.loc[index - 1, "Origin_City"] and
                    destination_city == reader.loc[index - 1, "Destination_City"]
                ):
                    continue

                if equipment == "DRY INTERMODAL":
                    continue
                
                final_templates += (
                    f'{origin_city.title()}, {origin_state} {origin_zip} > ' + 
                    f'{destination_city.title()}, {destination_state} {destination_zip}'
                    f'\n{int(float(carrier_miles))} miles'
                )

                length = ""
                if pd.isna(trailer_length) != True:
                    length = str(int(trailer_length))
                elif equipment.lower() == "straight truck":
                    length = "26"
                else:
                    length = "53"

                notes = ""
                if pd.isna(special_notes) != True:
                    notes = f'\n{special_notes}'
                    
                final_templates += (
                    f'\n{length} ft {equipment.title()} - {revenue.title()}'
                    f'{notes}'
                )

                final_templates += f'\nPick {ready_date} '
                if ready_date != ship_by:
                    final_templates += f'-{ship_by} '

                shipping = "07:00-15:00"
                #if pd.isna(internal_notes) != True:
                    #shipping = internal_notes
                #else:
                    #shipping = "07:00-15:00"    
                final_templates += shipping

                delivery = ""
                if pd.isna(receiver_appointment) != True:
                    delivery = str(receiver_appointment)[-5:]
                final_templates += f'\nDeliver {del_avail}'
                if del_avail == must_del:
                    final_templates += f' {delivery}'
                else:
                    final_templates += f'-{must_del} {delivery}'

                pay = ""
                if pd.isna(beginning_buy) != True:
                    pay = int(beginning_buy)
                else:
                    pay = ""
                final_templates += f"\nTracking must be maintained\n{weight} lbs\nPaying ${pay}\n\n\n"
            templates.write(final_templates)
        
def bulk_poster(filepath):
    with open(filepath, newline='') as infile, open("./bulk_posting.csv", "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        writer.writerow(
            ["Pickup Earliest*", "Pickup Latest", "Length (ft)*", "Weight (lbs)*", "Full/Partial*", "Equipment*", "Use Private Network*", "Private Network Rate",
            "Allow Private Network Booking", "Allow Private Network Bidding", "Use DAT Loadboard*", "Dat Loadboard Rate", "Allow DAT Loadboard Booking", 
            "Use Extended Network", "Contact Method*", "Origin City*", "Origin State*", "Origin Postal Code", "Destination City*", "Destination State*",
            "Destination Postal Code", "Comment", "Commodity", "Reference ID"]
        )
        for row in reader:
            mode = ""
            
            if row["Revenue"] == "TRUCKLOAD":
                mode = "Full"
            else:
                mode = "Partial"

            equipment = ""
            if row["Equipment"] == "VAN OR REEFER":
                equipment = "VR"
            elif row["Equipment"] == "FLATBED":
                equipment = "F"
            elif row["Equipment"] == "FLATBED W TARPS":
                equipment = "FT"
            elif row["Equipment"] == "REEFER":
                equipment = "R"
            elif row["Equipment"] == "STRAIGHT TRUCK":
                equipment = "SB"
            else:
                equipment = "V"

            length = ""
            if row["Trailer_Length"] != "":
                length = str(int(float(row["Trailer_Length"])))
            else:
                length = "53"

            writer.writerow([
                row["Ready_Date"], row["Ship_By_Date"], length, row["Weight"], mode, equipment, "no", "", "", "", "yes", "", "", "", "email",
                row["Origin_City"], row["Origin_State"], row["Origin_Zip"], row["Destination_City"], row["Destination_State"],
                row["Destination_Zip"], "", "", row["Id"]
            ])

def template_write_spi(filepath):
    with open(filepath, newline='') as f:
        reader = pd.read_csv(f)
        reader = reader.sort_values('Origin City')
        reader = reader.reset_index(drop=True)
        #print(reader)
        final_templates = ""
        with open("daily_templates.txt", "w") as templates:
            for index, row in reader.iterrows():
                if (
                    index != 0 and 
                    reader.loc[index, "Origin City"] == reader.loc[index - 1, "Origin City"] and
                    reader.loc[index, "Destination City"] == reader.loc[index - 1, "Destination City"]
                ):
                    continue

                final_templates += (
                    f'{reader.loc[index, "Origin City"]}, {reader.loc[index, "Origin State Code"]} {reader.loc[index, "Origin Postal Code"]} > ' +
                    f'{reader.loc[index, "Destination City"]}, {reader.loc[index, "Destination State Code"]} {reader.loc[index, "Destination Postal Code"]}' + 
                    f'\nPick {reader.loc[index, "Expected Ship Date"]}: {reader.loc[index, "First Stop Shipping Receiving Hours"]}'
                )
                final_templates += f'\nDeliver {reader.loc[index, "Expected Delivery Date"]} '
                if pd.isna(reader.loc[index, "Last Stop Appointment Time"]) != True:
                    final_templates += f'@ {reader.loc[index, "Last Stop Appointment Time"]}'
                elif pd.isna(reader.loc[index, "Last Stop Shipping Receiving Hours"]) != True:
                    final_templates += f'{reader.loc[index, "Last Stop Shipping Receiving Hours"]}'
                final_templates += f"\n\n{reader.loc[index, "Total Weight"]} lbs" + "\nPaying\n\n\n"
            templates.write(final_templates)
        
def bulk_poster_spi(filepath):
    with open(filepath, newline='') as infile, open("./bulk_posting.csv", "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        writer.writerow(
            ["Pickup Earliest*", "Pickup Latest", "Length (ft)*", "Weight (lbs)*", "Full/Partial*", "Equipment*", "Use Private Network*", "Private Network Rate",
            "Allow Private Network Booking", "Allow Private Network Bidding", "Use DAT Loadboard*", "Dat Loadboard Rate", "Allow DAT Loadboard Booking", 
            "Use Extended Network", "Contact Method*", "Origin City*", "Origin State*", "Origin Postal Code", "Destination City*", "Destination State*",
            "Destination Postal Code", "Comment", "Commodity", "Reference ID"]
        )
        for row in reader:
            mode = ""
            if row["Mode"] == "Truckload":
                mode = "Full"
            else:
                mode = "Partial"
            writer.writerow([
                row["Expected Ship Date"], row["Expected Ship Date"], "53", row["Total Weight"], mode, "V", "no", "", "", "", "yes", "", "", "", "email",
                row["Origin City"], row["Origin State Code"], row["Origin Postal Code"], row["Destination City"], row["Destination State Code"],
                row["Destination Postal Code"]
            ])


'''template_write(sys.argv[1])
bulk_poster(sys.argv[1])'''
    