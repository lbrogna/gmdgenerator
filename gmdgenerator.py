import os.path
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

chunk1 = ['***************************************************************\n',
          '* THIS FILE CONTAINS THE VALUES OF THE PARAMETERS REQUIRED    *\n',
          '* FOR THE GEOMOD MODULE, WHICH AUTOMATICALLY IS GENERATED IN  *\n',
          '* IDRISI. STRONGLY RECOMMEND REEDITING IN IDRISI IF NECESSARY.*\n',
          '***************************************************************\n',
          '\n',
          'TIME TO BEGIN GEOMOD, INCLUSIVE         :    xxx\n',
          'TIME TO END GEOMOD, INCLUSIVE           :    xxx\n',
          'TIME STEP IN TIME UNITS                 :    1\n',
          '\n',
          '# NEIGHBORS AWAY TO SEARCH,0=NO NIBBLE  :    0\n',
          'WRITE DEBUG OUTPUT TO LOG FILE,YES=1    :    0\n',
          'NAME OF STRATA/MASK IMAGE               :    xxx\n',
          'NAME OF INITIAL LANDUSE IMAGE           :    xxx\n',
          'DO ENVIR. IMPACT ANALYSIS? 1=YES, 0=NO  :    0\n',
          'CMP/READ SUITABILITY SCORES(0=CP,1=RD)  :    xxx\n',
          'NUMBER OF RUNS ONCE                     :    1\n']

chunk2a = ['NUMBER OF PERMANENT DRIVER IMAGES       :    xxx\n',
           'DRIVER IMAGE ?                          :    xxx\n',
           'SET OF DRIVER WEIGHTS FOR EACH RUN THRU GEOMOD\n',
           '   DRIVER?',
           '\n',
           '    0.2500',
           '\n']

chunk2b = ['SUITABILITY IMAGE FOR SIMULATION 1      :    xxx\n']

chunk3 = ['DO VALIDATION ANALYSIS? 1=YES, 0=NO     :    0\n',
          'SINCE NO VALIDATION IMAGE, LANDUSE CHANGE INFO READ FROM FOLLOWS:\n',
          '                                  LANDUSE STATE 1       LANDUSE STATE 2\n',
          'RGNVAL          REGION NAME    # CELLS      BEGIN        END      BEGIN        END\n']

chunk4 = ['\n',
          '# OF TIMES OF OUTPUT BESIDE END TIME    :    0\n',
          'NAME OF OUTPUT LANDUSE IMAGE            :    xxx\n']

strata = ['Region 1']
stratpath = 'N/A'

def open_csv(file_ext):
    """Open a CSV file."""
    text = file_ext.upper() + " Files"
    ext = "*." + file_ext
    filepath = askopenfilename(
        filetypes=[(text, ext), ("All Files", "*.*")]
    )
    if not filepath:
        return
    else:
        return filepath


def open_data():
    '''
    prompts user for path to .txt file containing loss data, sets up a global variable containing the path for future use
    '''
    path = open_csv("txt")
    data_path.config(text=os.path.basename(path))
    global datapath
    datapath = path


def get_data(path, strata, start_code, end_code, pers_code):
    '''
    :param path: path to the loss data provided by the user
    :param strata: list of strata
    :param start_code: first loss legend entry
    :param end_code: last loss legend entry
    :param pers_code: legend entry for persistence of state 1
    :return: list of dictionaries containing processed and categorized data
    '''
    with open(path, 'r') as fp:
        c_loss = {}
        v_loss = {}
        persistence1 = {}
        persistence2 = {}
        area = {}
        c = []
        v = []
        cal_end_code = start_code + int((len(range(start_code, end_code + 1)) / 2))
        val_start_code = cal_end_code + 1
        end_code = cal_end_code + int((len(range(start_code, end_code + 1)) / 2))
        for line in fp.readlines():
            line_list = line.strip().split()
            if str(strat_mode.get()) == "yes":
                if line_list[0] != 'Category' and line_list[0] != '0' and line_list[0] != 'Total':
                    stratum = int(line_list[0]) - 1
                    c_loss[strata[stratum]] = [int(loss) for loss in line_list[start_code + 1: cal_end_code + 2]]
                    v_loss[strata[stratum]] = [int(loss) for loss in line_list[val_start_code + 1: end_code + 2]]
                    persistence1[strata[stratum]] = int(line_list[pers_code + 1])
                    persistence2[strata[stratum]] = int(line_list[int(pers_cat2i.get(1.0, 'end-1c')) + 1])
                    area[strata[stratum]] = int(line_list[-1])
            if str(strat_mode.get()) == 'no':
                if line_list[0] != 'Category':
                    if int(line_list[0]) in range(start_code, cal_end_code):
                        c.append(int(line_list[1]))
                    elif int(line_list[0]) in range(cal_end_code, end_code):
                        v.append(int(line_list[1]))
                    elif int(line_list[0]) == 22:
                        p1 = int(line_list[1])
                    if int(line_list[0]) == int(pers_cat2i.get(1.0, 'end-1c')):
                        p2 = int(line_list[1])
        if str(strat_mode.get()) == 'no':
            a = sum(c) + sum(v) + p1 + p2
            c_loss['Region 1'] = c
            v_loss['Region 1'] = v
            persistence1['Region 1'] = p1
            persistence2['Region 1'] = p2
            area['Region 1'] = a
    return [c_loss, v_loss, persistence1, area, persistence2]


def open_drivers():
    '''
    prompts user for path to .rgf file of the driver images or .rst of suitability image, sets up a global variable
    containing the path for future use
    '''
    path = open_csv("r*")
    drivers_path.config(text=os.path.basename(path))
    global driverspath
    driverspath = path

def read_drivers(path):
    '''
    :param path: path for drivers .rgf file, or .rst for suitability image
    :return: a list of drivers if the input path is a .rgf file
    '''
    driverext = str(drivers_path)[-4:]
    if driverext == '.rgf':
        drivers = []
        linenum = 0
        with open(path, 'r') as fp:
            for line in fp.readlines():
                if linenum != 0:
                    drivers.append(line.strip())
                linenum += 1
        return drivers


def open_strat():
    '''
    prompts user for path to .rst file of the strata image, sets up a global variable containing the path for future use
    '''
    path = open_csv("rst")
    strat_path.config(text=os.path.basename(path))
    global stratpath
    stratpath = path.replace('.rst', '.rdc')
    global strata
    strata = read_strat(stratpath)

def read_strat(path):
    '''
    reads the strata from the provided .rgf file
    :param path: the path to the .rst file of the strata image
    :return: a list of strata names
    '''
    strata = []
    with open(path, 'r') as fp:
        for line in fp.readlines():
            line_list = line.strip().split()
            if line_list[0] == 'code':
                stratum = line[14:]
                strata.append(stratum.strip())
    return strata


def open_initials():
    '''
    prompts user for file path to initial driver image(s), either .rgf or .rst
    '''
    path = open_csv("r*")
    initials_path.config(text=os.path.basename(path))
    global initialspath
    initialspath = path


def read_initials(path):
    '''
    :param path: path for initials .rgf file containing ordered initial landcover images, or .rst containing one image
    :return: a list of initial landcover image names
    '''
    initials = []
    linenum = 0
    if initialspath[-4:] == '.rgf':
        with open(path, 'r') as fp:
            for line in fp.readlines():
                if linenum != 0:
                    initials.append(line.strip())
                linenum += 1
    if initialspath[-4:] == '.rst':
        initials.append(os.path.basename(initialspath))
    return initials


def quantities_from_data(strata, data):
    '''
    :param strata: a list of strata names
    :param data: the output of the get_data function, a list containing dictionaries of stratified data
    :return: a list of dictionaries containing quantities ready to be written to the new .gmd files
    '''
    state_2_b = {}
    state_2_e = {}
    state_1_e = {}
    state_1_b = {}
    c_loss_by_strata = data[0]
    v_loss_by_strata = data[1]
    persistence1_by_strata = data[2]
    for stratum in strata:
        # year = int(val_starti.get(1.0, 'end-1c')) - (
        #             int(val_endi.get(1.0, 'end-1c')) - int(val_starti.get(1.0, 'end-1c')))
        s1e = []
        s1b = []
        s2e = []
        s2b = []
        for start_year in range((int(val_endi.get(1.0, 'end-1c')) - int(val_starti.get(1.0, 'end-1c')))):
            if str(allocation_mode.get()) == 'dynamic':
                state_1_beg = persistence1_by_strata[stratum] + sum(v_loss_by_strata[stratum])
                state_2_beg = sum(c_loss_by_strata[stratum][start_year:])
                state_1_end = state_1_beg - state_2_beg
                state_2_end = state_2_beg * 2
            if str(allocation_mode.get()) == 'static':
                persistence2_by_strata = data[4]
                state_1_beg = persistence1_by_strata[stratum] + sum(v_loss_by_strata[stratum])
                state_2_beg = persistence2_by_strata[stratum] + sum(c_loss_by_strata[stratum])
                state_1_end = state_1_beg - sum(c_loss_by_strata[stratum][start_year:])
                state_2_end = state_2_beg + sum(c_loss_by_strata[stratum][start_year:])
            s1e.append(state_1_end)
            s2e.append(state_2_end)
            s2b.append(state_2_beg)
            s1b.append(state_1_beg)
            state_2_b[stratum] = s2b
            state_2_e[stratum] = s2e
            state_1_e[stratum] = s1e
            state_1_b[stratum] = s1b
    quantities = [state_1_b, state_1_e, state_2_b, state_2_e]
    return quantities


def write_to_editor():
    '''
    uses user inputs from right pane to write a template .gmd file to the edit pane
    '''
    # initials = read_initials(initialspath)
    driverext = driverspath[-4:]
    file_text = ""
    chunk1new = chunk1
    chunk1new[6] = chunk1new[6].replace('xxx', str(val_starti.get(1.0, 'end-1c')))
    if stratpath == 'N/A':
        chunk1new[12] = chunk1new[12].replace('xxx', 'N/A')
    else:
        chunk1new[12] = chunk1new[12].replace('xxx', os.path.basename(stratpath)[:-4])
    if driverext == '.rgf':
        chunk1new[15] = chunk1new[15].replace('xxx', '0')
    elif driverext == '.rst':
        chunk1new[15] = chunk1new[15].replace('xxx', '1')
    for line in chunk1new:
        file_text += line
    if driverext == '.rgf':
        drivers = read_drivers(driverspath)
        chunk2new = chunk2a[0].replace('xxx', str(len(drivers)))
        for driver in drivers:
            new_driver = chunk2a[1]
            new_driver = new_driver.replace('?', str(drivers.index(driver) + 1)).replace('xxx', driver)
            chunk2new += new_driver
        new_weight_table = ['', '']
        weight = "{:.4f}".format(float(1 / len(drivers)))
        for driver in drivers:
            new_driver = chunk2a[3].replace('?', str(drivers.index(driver) + 1))
            new_weight_table[0] += new_driver
            new_weight_table[1] += chunk2a[5].replace('0.2500', str(weight))
        for line in new_weight_table:
            chunk2new += line + '\n'
    if driverext == '.rst':
        chunk2new = chunk2b[0].replace('xxx', os.path.basename(driverspath))
    file_text += chunk2new
    for line in chunk3:
        file_text += line
    data = get_data(path=datapath, strata=strata, start_code=int(loss_cat1i.get(1.0, 'end-1c')),
                    end_code=int(loss_cat2i.get(1.0, 'end-1c')), pers_code=int(pers_cat1i.get(1.0, 'end-1c')))
    quantities = quantities_from_data(strata, data)
    state_1_b = quantities[0]
    strat_area = data[3]
    for stratum in strata:
        rgn_val = str(strata.index(stratum) + 1).rjust(6)
        strat_name = stratum.rjust(21)
        num_cells = str(strat_area[stratum]).rjust(11)
        placeholder = (str('xxx').rjust(11)) * 4
        new_strata = rgn_val + strat_name + num_cells + placeholder + '\n'
        file_text += new_strata
    prefix = prefixi.get(1.0, 'end-1c')
    suffix = suffixi.get(1.0, 'end-1c')
    chunk4new = chunk4
    chunk4new[2] = chunk4[2].replace('xxx', prefix + 'xxx' + suffix)
    for line in chunk4new:
        file_text += line
    output_txt.insert(END, file_text)


def write_and_save():
    '''
    writes the text from the edit pane to a batch of .gmd files each one with different values, then saves those files to a destination folder
    '''
    path = asksaveasfilename(
        filetypes=((".GMD files", "*.gmd"), ("All files", "*.*")),
        title="Save .gmd files with suffix...",
    )
    initials = read_initials(initialspath)
    data = get_data(path=datapath, strata=strata, start_code=int(loss_cat1i.get(1.0, 'end-1c')), end_code=int(loss_cat2i.get(1.0, 'end-1c')), pers_code=int(pers_cat1i.get(1.0, 'end-1c')))
    quantities = quantities_from_data(strata, data)
    state_1_b = quantities[0]
    state_1_e = quantities[1]
    state_2_b = quantities[2]
    state_2_e = quantities[3]
    max_cal_length = int(val_endi.get(1.0, 'end-1c')) - int(val_starti.get(1.0, 'end-1c'))
    val_start = int(val_starti.get(1.0, 'end-1c'))
    indexer = 0
    for cal_length in range(max_cal_length, 0, -1):
        new_path = str(path) + '_cal_len_' + str(cal_length) + '.gmd'
        line_list = output_txt.get(1.0, 'end-1c').split('\n')
        with open(new_path, 'w+') as fn:
            for line in line_list:
                line_label = line.split(':')[0]
                if line_label == 'TIME TO END GEOMOD, INCLUSIVE           ':
                    line = line.replace('xxx', str(cal_length + val_start))
                    fn.write(line + '\n')
                elif line_label == 'NAME OF INITIAL LANDUSE IMAGE           ' and initialspath[-4:] == '.rgf':
                    line = line.replace('xxx', initials[cal_length - 1])
                    fn.write(line + '\n')
                elif line_label == 'NAME OF INITIAL LANDUSE IMAGE           ' and initialspath[-4:] == '.rst':
                    line = line.replace('xxx', initials[0])
                    fn.write(line + '\n')
                elif line_label == 'NAME OF OUTPUT LANDUSE IMAGE            ':
                    line = line.replace('xxx', '_cal_len' + str(cal_length))
                    fn.write(line + '\n')
                elif line[6:27].strip() in strata:
                    stratum = line[6:27].strip()
                    s1b = str(state_1_b[stratum][indexer]).rjust(11)
                    s1e = str(state_1_e[stratum][indexer]).rjust(11)
                    s2b = str(state_2_b[stratum][indexer]).rjust(11)
                    s2e = str(state_2_e[stratum][indexer]).rjust(11)
                    placeholder = 'xxx'.rjust(11)
                    line = line.replace(placeholder, s1b, 1)
                    line = line.replace(placeholder, s1e, 1)
                    line = line.replace(placeholder, s2b, 1)
                    line = line.replace(placeholder, s2e, 1)
                    fn.write(line + '\n')
                else:
                    fn.write(line + '\n')
        fn.close()
        print(new_path)
        indexer += 1


def configure_amode():
    '''
    configures UI based on user's choice of allocation mode
    '''
    if str(allocation_mode.get()) == 'static':
        lossb_message.configure(text='.rst for initial landcover image')
        driver_message.configure(text=".rgf file for driver variables OR .rst for existing suitability image")
    if str(allocation_mode.get()) == 'dynamic':
        lossb_message.configure(text='.rgf for initial landcover images (ordered from shortest to longest cal. period)')
        driver_message.configure(text=".rgf file for driver variables")



def configure_smode():
    '''
    configures UI based on user's choice of stratification mode
    '''
    if strat_mode.get() == "yes":
        open_strat.configure(state=ACTIVE)
        data_file_messagel.configure(text='loss data (.txt tabular CrossTab output for loss image/strata image):')
    if strat_mode.get() == "no":
        open_strat.configure(state=DISABLED)
        data_file_messagel.configure(text='loss data (.txt tabular Area output for loss image):')


# code for UI
window = Tk()
window.title("Multiple Calibration Analysis .gmd File Creator")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

left_frame = Frame(window, relief=RAISED, bd=2)
left_frame.grid(row=0, column=0, sticky="ns")
session_parametersl = Label(left_frame, text="Session Parameters", font=('Arial', 9, 'bold', 'underline'))
session_parametersl.grid(row=0, column=0, columnspan=2)
strat_mode = StringVar()
allocation_mode = StringVar()
a_mode1 = Radiobutton(left_frame, text="a-Mode: Static", state='normal', variable=allocation_mode, value='static',
                      command=configure_amode)
a_mode2 = Radiobutton(left_frame, text="a-Mode: Dynamic", state='normal', variable=allocation_mode, value='dynamic',
                      command=configure_amode)
a_mode1.grid(row=1, column=0, sticky="ew")
a_mode2.grid(row=1, column=1, sticky="ew")
s_mode1 = Radiobutton(left_frame, text="s-Mode: Unstratified", state='normal', variable=strat_mode, value='no',
                      command=configure_smode)
s_mode2 = Radiobutton(left_frame, text="s-Mode: Stratified", state='normal', variable=strat_mode, value='yes',
                      command=configure_smode)
s_mode1.grid(row=2, column=0, sticky="ew")
s_mode2.grid(row=2, column=1, sticky="ew")
datesl = Label(left_frame, text="i. Dates", font=('Arial', 9, 'underline'))
datesl.grid(row=3, column=0, columnspan=2)
val_startl = Label(left_frame, text="validation start time")
val_startl.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
val_endl = Label(left_frame, text="validation end time")
val_endl.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
val_starti = Text(left_frame, height=1, width=5)
val_starti.grid(row=5, column=0)
val_endi = Text(left_frame, height=1, width=5)
val_endi.grid(row=5, column=1)
output_namesl = Label(left_frame, text="ii. Simulation Output Naming Convention", font=('Arial', 9, 'underline'))
output_namesl.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5)
prefixl = Label(left_frame, text="prefix:")
prefixl.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
suffixl = Label(left_frame, text="suffix:")
suffixl.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
prefixi = Text(left_frame, height=1, width=9)
prefixi.grid(row=8, column=0)
suffixi = Text(left_frame, height=1, width=9)
suffixi.grid(row=8, column=1)
file_headerl = Label(left_frame, text="iii. Loss Data", font=('Arial', 9, 'underline'))
file_headerl.grid(row=9, column=0, columnspan=2)
data_filel = Label(left_frame, text="a. Loss Areas", font=('Arial', 9, 'italic'))
data_filel.grid(row=11, column=0, columnspan=2, sticky="ew")
data_file_messagel = Label(left_frame, text="loss data:", font=('Arial', 7))
data_file_messagel.grid(row=12, column=0, columnspan=2, sticky="ew")
data_path = Label(left_frame, anchor="w", text="", font=('Arial', 8), width=20)
data_path.grid(row=14, column=1, sticky="w", pady=5)
open_data = Button(left_frame, text='Open', height=1, width=10, command=open_data)
open_data.grid(row=14, column=0, sticky="w", padx=5)
legend_messagel = Label(left_frame, text="b. Legend Info", font=('Arial', 9, 'italic'))
legend_messagel.grid(row=15, column=0, columnspan=2, sticky="ew")
loss_cat1l = Label(left_frame, text="first loss legend code")
loss_cat1l.grid(row=16, column=0, sticky="ew", padx=5, pady=5)
loss_cat2l = Label(left_frame, text="last loss legend code")
loss_cat2l.grid(row=16, column=1, sticky="ew", padx=5, pady=5)
loss_cat1i = Text(left_frame, height=1, width=5)
loss_cat1i.grid(row=17, column=0)
loss_cat2i = Text(left_frame, height=1, width=5)
loss_cat2i.grid(row=17, column=1)
pers_cat1l = Label(left_frame, text="state1 pers. legend code")
pers_cat1l.grid(row=18, column=0, sticky="ew", padx=5, pady=5)
pers_cat2l = Label(left_frame, text="state2 pers. legend code")
pers_cat2l.grid(row=18, column=1, sticky="ew", padx=5, pady=5)
pers_cat1i = Text(left_frame, height=1, width=5)
pers_cat1i.grid(row=19, column=0)
pers_cat2i = Text(left_frame, height=1, width=5)
pers_cat2i.grid(row=19, column=1)
driver_headerl = Label(left_frame, text="iv. Driver Variables or Suitability Image", font=('Arial', 9, 'underline'))
driver_headerl.grid(row=20, column=0, columnspan=2)
driver_message = Label(left_frame, text=".rgf file for driver variables", font=('Arial', 7))
driver_message.grid(row=21, column=0, columnspan=2, sticky="ew")
drivers_path = Label(left_frame, anchor="w", text="", font=('Arial', 8), width=20)
drivers_path.grid(row=22, column=1, sticky="w", pady=5)
open_drivers = Button(left_frame, text='Open', height=1, width=10, command=open_drivers)
open_drivers.grid(row=22, column=0, sticky="w", padx=5)
lossa_headerl = Label(left_frame, text="v. Additional Information", font=('Arial', 9, 'underline'))
lossa_headerl.grid(row=23, column=0, columnspan=2)
lossa_message = Label(left_frame, text='.rdc for strata image:', font=('Arial', 7))
lossa_message.grid(row=25, column=0, columnspan=2, sticky="ew")
strat_path = Label(left_frame, anchor="w", text="", font=('Arial', 8), width=20)
strat_path.grid(row=26, column=1, sticky="w", pady=5)
open_strat = Button(left_frame, text='Open', height=1, width=10, command=open_strat)
open_strat.grid(row=26, column=0, sticky="w", padx=5)
lossb_message = Label(left_frame,
                      text="initial landcover image(s)",
                      font=('Arial', 7))
lossb_message.grid(row=27, column=0, columnspan=2, sticky="ew")
initials_path = Label(left_frame, anchor="w", text="", font=('Arial', 8), width=20)
initials_path.grid(row=28, column=1, sticky="w", pady=5)
open_initials = Button(left_frame, text='Open', height=1, width=10, command=open_initials)
open_initials.grid(row=28, column=0, sticky="w", padx=5)
file_messagel = Label(left_frame, text="(all files should be in or connected to Terrset working folder)",
                      font=('Arial', 7, 'bold'))
file_messagel.grid(row=29, column=0, columnspan=2, sticky="ew")

right_frame = Frame(window)
right_frame.grid(row=0, column=1, sticky="ns")
output_txt = Text(right_frame,
                  height=35,
                  width=100,
                  bg="WHITE")
output_txt.grid(row=0, column=0, columnspan=3, sticky="ne")

preview = Button(right_frame, text="preview and edit", command=write_to_editor)
preview.grid(row=1, column=0)
save = Button(right_frame, text='save file batch', command=write_and_save)
save.grid(row=1, column=1)

window.mainloop()
