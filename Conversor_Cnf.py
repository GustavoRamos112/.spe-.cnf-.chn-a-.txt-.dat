import numpy as np
import time
import struct
import Func
import Mensajes


def read_cnf_file(filename, sep):
    # Dictionary with all the information read
    read_dic = {}
    #with open(filename, 'rb') as f:
    f = open(filename, 'rb')
    i = 0
    while True:
        # List of available section headers
        sec_header = 0x70 + i*0x30
        i += 1
        # Section id in header
        sec_id_header = uint32_at(f, sec_header)

        # End of section list
        if sec_id_header == 0x00:
            break

        # Location of the begining of each sections
        sec_loc = uint32_at(f, sec_header+0x0a)
        # Known section id's:
        # Parameter section (times, energy calibration, etc)
        if sec_id_header == 0x00012000:
            offs_param = sec_loc
            read_dic.update(get_energy_calibration(f, offs_param))
            read_dic.update(get_date_time(f, offs_param))
            read_dic.update(get_shape_calibration(f, offs_param))
        # String section
        elif sec_id_header == 0x00012001:
            offs_str = sec_loc
            read_dic.update(get_strings(f, offs_str))
        # Marker section
        elif sec_id_header == 0x00012004:
            offs_mark = sec_loc
            read_dic.update(get_markers(f, offs_mark))
        # Channel data section
        elif sec_id_header == 0x00012005:
            offs_chan = sec_loc
            read_dic.update(get_channel_data(f, offs_param, offs_chan))
        else:
            continue

        # For known sections: section header ir repeated in section block
        if (sec_id_header != uint32_at(f, sec_loc)):
            print('File {}: Format error\n'.format(filename))
    f.close()
    # Once the file is read, some derived magnitudes can be obtained

    # Convert channels to energy
    if set(("Channels", "Energy coefficients")) <= set(read_dic):
        read_dic.update(chan_to_energy(read_dic))

    # Compute ingegration between markers
    if set(("Channels", "Left marker")) <= set(read_dic):
        read_dic.update(markers_integration(read_dic))

    """ print(50*"=")
    print(f"{' '*10}File {filename} succesfully read!{' '*10}")
    print(50*"=") """

    write_to_file(filename, read_dic, sep)

    return read_dic

##########################################################
# Definitions for reading some data types
##########################################################


def uint8_at(f, pos):
    f.seek(pos)
    return np.fromfile(f, dtype=np.dtype("<u1"), count=1)[0]


def uint16_at(f, pos):
    f.seek(pos)
    return np.fromfile(f, dtype=np.dtype("<u2"), count=1)[0]


def uint32_at(f, pos):
    f.seek(pos)
    return np.fromfile(f, dtype=np.dtype("<u4"), count=1)[0]


def uint64_at(f, pos):
    f.seek(pos)
    return np.fromfile(f, dtype=np.dtype("<u8"), count=1)[0]


def pdp11f_at(f, pos):
    """
    Convert PDP11 32bit floating point format to
    IEE 754 single precision (32bits)
    """
    f.seek(pos)
    # Read two int16 numbers
    tmp16 = np.fromfile(f, dtype=np.dtype("<u2"), count=2)
    # Swapp positions
    mypack = struct.pack("HH", tmp16[1], tmp16[0])
    f = struct.unpack("f", mypack)[0]/4.0
    return f


def time_at(f, pos):
    return ~uint64_at(f, pos)*1e-7


def datetime_at(f, pos):
    return uint64_at(f, pos) / 10000000 - 3506716800


def string_at(f, pos, length):
    f.seek(pos)
    # In order to avoid characters with not utf8 encoding
    return f.read(length).decode("utf8").rstrip("\00").rstrip()

###########################################################
# Definitions for locating and reading data inside the file
###########################################################


def get_strings(f, offs_str):
    
    sample_name = string_at(f, offs_str + 0x0030, 0x40)
    sample_id = string_at(f, offs_str + 0x0070, 0x10)
    # sample_id   = string_at(f, offs_str + 0x0070, 0x40)
    sample_type = string_at(f, offs_str + 0x00b0, 0x10)
    sample_unit = string_at(f, offs_str + 0x00c4, 0x40)
    user_name = string_at(f, offs_str + 0x02d6, 0x18)
    sample_desc = string_at(f, offs_str + 0x036e, 0x100)

    out_dic = {
               "Sample name": sample_name,
               "Sample id": sample_id,
               "Sample type": sample_type,
               "Sample unit": sample_unit,
               "User name": user_name,
               "Sample description": sample_desc
              }

    return out_dic


def get_energy_calibration(f, offs_param):
    """Read energy calibration coefficients."""

    offs_calib = offs_param + 0x30 + uint16_at(f, offs_param + 0x22)
    A = np.empty(4)
    A[0] = pdp11f_at(f, offs_calib + 0x44)
    A[1] = pdp11f_at(f, offs_calib + 0x48)
    A[2] = pdp11f_at(f, offs_calib + 0x4c)
    A[3] = pdp11f_at(f, offs_calib + 0x50)

    # Assuming a maximum length of 0x11 for the energy unit
    energy_unit = string_at(f, offs_calib + 0x5c, 0x11)

    # MCA type
    MCA_type = string_at(f, offs_calib + 0x9c, 0x10)

    # Data source
    data_source = string_at(f, offs_calib + 0x108, 0x10)

    out_dic = {"Energy coefficients": A,
               "Energy unit": energy_unit,
               "MCA type": MCA_type,
               "Data source": data_source
               }

    return out_dic


def get_shape_calibration(f, offs_param):
    """
    Read Shape Calibration Parameters :
        FWHM=B[0]+B[1]*E^(1/2)  . B[2] and B[3] probably tail parameters
    """

    offs_calib = offs_param + 0x30 + uint16_at(f, offs_param + 0x22)
    B = np.empty(4)
    B[0] = pdp11f_at(f, offs_calib + 0xdc)
    B[1] = pdp11f_at(f, offs_calib + 0xe0)
    B[2] = pdp11f_at(f, offs_calib + 0xe4)
    B[3] = pdp11f_at(f, offs_calib + 0xe8)

    out_dic = {"Shape coefficients": B}

    return out_dic


def get_channel_data(f, offs_param, offs_chan):
    """Read channel data."""

    # Total number of channels
    n_channels = uint8_at(f, offs_param + 0x00ba) * 256
    # Data in each channel
    f.seek(offs_chan + 0x200)
    chan_data = np.fromfile(f, dtype="<u4", count=n_channels)
    # Total counts of the channels
    total_counts = np.sum(chan_data)
    # Measurement mode
    meas_mode = string_at(f, offs_param + 0xb0, 0x03)

    # Create array with the correct channel numbering
    channels = np.arange(1, n_channels+1, 1)

    out_dic = {"Number of channels": n_channels,
               "Channels data": chan_data,
               "Channels": channels,
               "Total counts": total_counts,
               "Measurement mode": meas_mode
               }

    return out_dic


def get_date_time(f, offs_param):
    """Read date and time."""

    offs_times = offs_param + 0x30 + uint16_at(f, offs_param + 0x24)

    start_time = datetime_at(f, offs_times + 0x01)
    real_time = time_at(f, offs_times + 0x09)
    live_time = time_at(f, offs_times + 0x11)

    # Convert to formated date and time
    start_time_str = time.strftime("%d-%m-%Y, %H:%M:%S", time.gmtime(start_time))

    out_dic = {"Real time": real_time,
               "Live time": live_time,
               "Start time": start_time_str
               }
    return out_dic


def get_markers(f, offs_mark):
    """Read left and right markers."""

    # TODO: not working properly
    marker_left = uint32_at(f, offs_mark + 0x007a)
    marker_right = uint32_at(f, offs_mark + 0x008a)

    out_dic = {"Left marker": marker_left,
               "Right marker": marker_right,
               }

    return out_dic


def chan_to_energy(dic):
    """ Convert channels to energy using energy calibration coefficients."""

    A = dic['Energy coefficients']
    ch = dic['Channels']
    energy = A[0] + A[1]*ch + A[2]*ch*ch + A[3]*ch*ch*ch

    out_dic = {"Energy": energy}

    return out_dic


def markers_integration(dic):
    # Count between left and right markers
    # TODO: check integral counts limits
    chan_data = dic['Channels data']
    l_marker = dic['Left marker']
    r_marker = dic['Right marker']
    marker_counts = np.sum(chan_data[l_marker-1:r_marker-1])

    out_dic = {"Counts in markers": marker_counts}

    return out_dic

###########################################################
# Format of the output text file
###########################################################


def write_to_file(filename, dic, sep):
    _name, carpet = Func.clear_name(filename)
    name = _name[:-4]
    Func.Crear_carpeta(f'{carpet}{name}')

    f = open(f'{carpet}{name}/{name}.txt', "w")
    f.write("#\n")
    f.write(f"# Sample name: {dic['Sample name']}\n")
    f.write("\n")

    f.write(f"# Sample id: {dic['Sample id']}\n")
    f.write(f"# Sample type: {dic['Sample type']}\n")
    f.write(f"# User name: {dic['User name']}\n")
    f.write(f"# Sample description: {dic['Sample description']}\n")
    f.write("#\n")

    f.write(f"# Start time: {dic['Start time']}\n")
    f.write(f"# Real time (s): {dic['Real time']}\n")
    f.write(f"# Live time (s): {dic['Live time']}\n")
    f.write("#\n")

    f.write(f"# Total counts: {dic['Total counts']}\n")
    f.write("#\n")

    f.write(f"# Left marker: {dic['Left marker']}\n")
    f.write(f"# Right marker: {dic['Right marker']}\n")
    f.write(f"# Counts: {dic['Counts in markers']}\n")
    f.write("#\n")

    f.write("# Energy calibration coefficients (E = sum(Ai * n**i))\n")
    for j, co in enumerate(dic['Energy coefficients']):
        f.write(f"#    A{j} = {co}\n")
    f.write(f"# Energy unit: {dic['Energy unit']}\n")
    f.write("#\n")

    f.write("# Shape calibration coefficients (FWHM = B0 + B1*E^(1/2)  Low Tail= B2 + B3*E)\n")
    for j, co in enumerate(dic['Shape coefficients']):
        f.write(f"#    B{j} = {co}\n")
    f.write(f"# Energy unit: {dic['Energy unit']}\n")
    f.write("#\n")

    f.write("# Channel data\n")
    f.write(f"#\tn\tenergy({dic['Energy unit']})\tcounts\trate(1/s)\n")
    f.write(f"#{'-'*50}\n")
    g = open(f'{carpet}{name}/{name}_datos.dat', "w")
    for i, j, k in zip(dic['Channels'], dic['Energy'], dic['Channels data']):
        f.write(f"{i}{sep}{j}{sep}{k}{sep}{k/dic['Live time']}\n")
        g.write(f"{i}{sep}{j}{sep}{k}{sep}{k/dic['Live time']}\n")
    
    g.close()
    f.close()


if __name__ == "__main__":

    """ name = "prub/bkg_290617.CNF"

    c = read_cnf_file(name, ', ')

    print(f"Sample id: {c['Sample id']}")
    print(f"Measurement mode: {c['Measurement mode']}")

    chan = c['Channels']
    n_chan = c['Number of channels']
    chan_data = c['Channels data']
    energy = c['Energy']
    print("Number of channels used: {n_chan}")

    # Testing channels and energy calibration
    inchan = 250
    print(f"At channel {inchan}:")
    print(f"\t Counts: {chan_data[np.where(chan == inchan)][0]}")
    print(f"\t Energy: {energy[np.where(chan == inchan)][0]}")

    if True:
        import matplotlib.pyplot as plt
        fig1 = plt.figure(1, figsize=(8, 8))

        ax1 = fig1.add_subplot(111)
        ax1.set_xlabel(u"Channels")
        ax1.set_ylabel(u"Counts")
        ax1.plot(chan, chan_data, "k.")
        ax1.set_title("File read: " + filename)

        plt.show() """