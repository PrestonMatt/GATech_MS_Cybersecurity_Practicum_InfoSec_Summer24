from os import getcwd

remove_strs = [
    # Notes:
    "6-29", "#1 & 2 coded in SDI", "Revised by Supp 11", "See Note [4]", "SDI 1=L/SDI 2=R", "See Note [5]", "6-27",
    "No. 5 to 8 in SDI", "No. 1 to 4 in SDI – 6-26", "No. 9 to 12 in SDI – 6-26", "No. 13 to 16 in SDI – 6-26",
    "6-49", "6-11", "6-50", "6-21 and ARINC 735", "6-22 and ARINC 735", "6-23 and ARINC 735", "See ARINC 741",
    "6-30", "6-12", "SDI-01=left/SDI-10=right", "6-13/6-27", "Per ARINC 522A", "See Attachment 10",
    "6-6/6-27", "SDI 1= A/SDI 2= B", "6-7/6-27", "6-24/6-27", "6-20", "6-28", "See ARINC 604", "6-31", "See ARINC 743A",
    "6-35", "See ARINC Rpt 610", "6-19", "Zero for A-321", "See Note [5]", "6-52", "6-14", "6-51", "See ARINC 429P2",
    "Used only in simulator", "See ARINC 735", "See Att. 6 for SDI encoding", "Engine Types: P&W", "Engine Types: GE",
    "Bit 11-Chan. A", "Bit 12-Chan. B", "6-33", "See Notes [6] & [7]", "See Note [6]", "6-2-1", "No. 13 to 16 in SDI – 6-26",
    # Pos Sense:
    "UP", "Climb", "OPEN", "TE Down", "Above Cmd Alt", "above sel alt",
    # Units:
    "Ft/Min", "Deg/180", "Volts", "Deg C", "Deg", "Mach", "Feet", "% MAC", "% RPM", "Knots", "RPM", "PSIA",
    "Lb./Ft.", "N.M.", "Degrees", "Deg/Sec", "Meters", "in/sec", "% N1/Deg", "% FS", "% N1Nom", "% N1 Nom",
    " % ", "Seconds", "See Sec. 3.1.4", "LBF", "Gs", "VDC",
    "Hr:Min:S", "mV", "mB", "PSI", "VDC", "DDM", "Dots", "US Pint", " mb ", "Nmiles", "M/minute", "Lbs.",
    "Minute", "in. Hg", "Lbs/hr", "pph", "PPH", "MSEC", "Ratio", "PF", "NM", "Min.", "Lb/Gal", " g ",
    "Gal.", "Lbs/Gal", "Inches", "Lb/Hr", "Flights", "Scalar", "DFN/%N1",
    # Params:
    "Selected Vertical Speed", "Right/PDU Flap", "DC Voltage (Battery)", "Right Outboard Flap Position",
    "Selected Runway Heading", "Left/PDU Slat", "Oil Temp. Input (IDG/CSD)", "Left Inboard Flap Position",
    "Selected", "Right/PDU Slat", "Right Inboard Flap Position", "Cruise Altitude", "Flap/Slat Lever",
    "Flap Lever Position-median value", "Long. Zero Fuel Ctr of Gravity", "Course #2", "GNSS Latitude",
    "Flap Lever Position - Center", "GNSS Longitude", "Runway Length", "GNSS Ground Speed", "EPR", "TBD",
    "N1", "Flap Lever Position - Left", "Desired Track", "Brake Temp. (Left Inner L/G)", "Ambient Pressure",
    "Pamb Sensor", "Flap Lever Position - Right", "Wheel Torque Output", "Ambient Static Pressure",
    "Ambient Pressure", "Waypoint Bearing", "Brake Temp. (Left Outer L/G)", "Fuel Temperature",
    "Cross Track Distance", "Horizontal GLS Deviation Rectilinear", "Brake Temp. (Right Inner L/G)",
    "No. 13", "to 16 in SDI", " \– 6-26", "Cross Track Deviation", "Vertical Deviation", "North-South Velocity-Magnetic",
    "East-West Velocity-Magnetic", "Position-5"
]

dir_ = getcwd()
with open(r"C:\Users\mspre\Desktop\Practicum Resources\GATech_MS_Cybersecurity_Practicum_InfoSec_Summer24\Documentation\Labels\raw_BNR.txt","r") as fd:
    lines = fd.readlines()
    with open(dir_ + r"\bnr_processed.txt", "w") as b_fd:
        prev_line = ""
        new_line = ""
        label = ""
        for line in lines:
            if(prev_line == "\n"): # New octal label.
                line = "0o" + line.replace(" ","").replace("\n","") + ":\n"
                label = line.strip("\n")
            else:
                line.replace(" to ", "-")
                if(line == "\n"):
                    prev_line = line
                    b_fd.write(line)
                    continue
                for rstr in remove_strs:
                    line = line.replace(rstr, "")
                try:
                    hex_ = "0x" + line[0] + line[2] + line[4]
                    #print(hex_)
                except IndexError:
                    print(line)
                    cont = input()
                l = line.split(" ")[3:]
                #print(l)
                new_l = [label, hex_]
                for item in l:
                    if(item.__contains__("+") or
                       item == ("1/32") or item == ("1/64")
                       or item.__contains__("0.9536743") or
                       #item == "X" or
                       item.__contains__("\n")): #or
                       #item == "A" or
                       #item == "B" or
                       #item == "C" or
                       #item == "D" or
                       #item == "E" or
                       #item == "F"):
                            new_l.append(item)
                    elif(item.__contains__("-")):
                        try:
                            s = float(item.split("-")[0])
                        except ValueError:
                            pass
                    else:
                        try:
                            element = float(item)
                            new_l.append(element)
                        except:
                            pass
                print(line.strip("\n"))
                print(new_l)
                try:
                    res = new_l[4]
                    digits = int(new_l[3])
                    if(str(new_l[2]).__contains__("-")):
                        range_ = new_l[2].replace("-",", ")
                    else:
                        range_ = "0.0, " + str(new_l[2])
                except IndexError:
                    res = "'***'"
                    digits = "'***'"
                    range_ = "'***'"
                except ValueError:
                    res = "'***'"
                    digits = "'***'"
                    range_ = "'***'"
                    
                newline = hex_ + f': ["BNR", {res}, ({range_}), {digits}],\n'
                line = newline
                #cont = input(newline)
                """
                l = line.split(" ")
                new_l = []
                for item in l:
                    try:
                        if(item.__contains__("-")):
                            new_l.append(item)
                        else:
                            new_l.append(float(item))
                    except ValueError:
                        pass
                for ite in new_l:
                    new_line += str(ite) + " "
                """
            prev_line = line # should be unaffected by the above
            # ^ If it's just solely a new line char.
            b_fd.write(line)
        b_fd
    b_fd.close()
fd.close()
