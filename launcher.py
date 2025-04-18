import PySimpleGUI as sg
import numpy as np

application_name = "3 Field Breast Field Matcher"

def alpha_theta_calculator(med_tan_gantry, lat_tan_gantry, med_tan_Y2, lat_tan_Y2):
    if med_tan_gantry <= np.pi/2 and med_tan_gantry >= 0:
        breast_laterality = "right"
    elif med_tan_gantry >= 2 / 3 * np.pi and med_tan_gantry <= 2 * np.pi:
        breast_laterality = "left"
    else:
        breast_laterality = "unknown"
        print("Error: angles do not correlate with expected breast tangent fields.")
        return

    if med_tan_gantry <= np.pi/2:
        med_tan_angle_to_cax = med_tan_gantry
    elif med_tan_gantry > np.pi/2 and med_tan_gantry <= 3 /2 * np.pi:
        med_tan_angle_to_cax = abs(np.pi - med_tan_gantry)
    elif med_tan_gantry > 3 / 2 * np.pi and med_tan_gantry <= 2 * np.pi:
        med_tan_angle_to_cax = 2 * np.pi - med_tan_gantry
    else:
        print("Error: provided angle of medial tangent gantry angle outside of expected values (0-360).")
        return

    if lat_tan_gantry <= np.pi / 2:
        lat_tan_angle_to_cax = lat_tan_gantry
    elif lat_tan_gantry > np.pi / 2 and lat_tan_gantry <= 3 / 2 * np.pi:
        lat_tan_angle_to_cax = abs(np.pi - lat_tan_gantry)
    elif lat_tan_gantry > 3 / 2 * np.pi and lat_tan_gantry <= 2 * np.pi:
        lat_tan_angle_to_cax = 2 * np.pi - lat_tan_gantry
    else:
        print("Error: provided angle of lateral tangent gantry angle outside of expected values (0-360).")
        return

    med_tan_alpha = np.arctan(med_tan_Y2/100)
    lat_tan_alpha = np.arctan(lat_tan_Y2/100)

    return med_tan_angle_to_cax, lat_tan_angle_to_cax, med_tan_alpha, lat_tan_alpha, breast_laterality

def collimator_angle_calculator(theta, alpha, field, breast_laterality):
    angle_col = np.arcsin(np.tan(alpha)/np.tan(theta))
    if breast_laterality == "right":
        return abs(np.rad2deg(2 * np.pi - angle_col))
    else:
        return abs(np.rad2deg(angle_col))

def couch_angle_calculator(theta, alpha, field, breast_laterality):
    angle_couch = np.arcsin(np.sin(alpha)/np.sin(theta))
    if breast_laterality == "right":
        if field == "med":
            return abs(np.rad2deg(2*np.pi - angle_couch))
        else:
            return np.rad2deg(angle_couch)
    if breast_laterality == "left":
        if field == "lat":
            return abs(np.rad2deg(2*np.pi - angle_couch))
        else:
            return np.rad2deg(angle_couch)

def launcher():
    layout = [
        [sg.Text("Gantry Angle - Medial Tangent: "), sg.InputText(key="med_tan_gantry", size=(5,1), enable_events=True)],
        [sg.Text("Gantry Angle - Lateral Tangent:"), sg.InputText(key="lat_tan_gantry", size=(5,1), enable_events=True)],
        [sg.Text("Y2 - Medial Tangent: "), sg.InputText(key="med_tan_Y2", size=(4,1), enable_events=True)],
        [sg.Text("Y2 - Lateral Tangent:"), sg.InputText(key="lat_tan_Y2", size=(4,1), enable_events=True)],
        [sg.Text("Medial Tangent Collimator: "), sg.Text("0.00", key="med_tan_col")],
        [sg.Text("Lateral Tangent Collimator:"), sg.Text("0.00", key="lat_tan_col")],
        [sg.Text("Medial Tangent Couch: "), sg.Text("0.00", key="med_tan_couch")],
        [sg.Text("Lateral Tangent Couch:"), sg.Text("0.00", key="lat_tan_couch")],
        [sg.Button("Calculate"), sg.Button("Exit"), sg.Text(size=[10, 1])],
    ]
    window = sg.Window(application_name, layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        if event == "Calculate":
            # Convert all string inputs into numbers and convert angles to radians for ease of calculation
            med_tan_gantry = np.deg2rad(float(values['med_tan_gantry']))
            lat_tan_gantry = np.deg2rad(float(values['lat_tan_gantry']))
            med_tan_Y2 = float(values['med_tan_Y2'])
            lat_tan_Y2 = float(values['lat_tan_Y2'])

            # Pass new floats to angle calculator
            [
                med_tan_theta,
                lat_tan_theta,
                med_tan_alpha,
                lat_tan_alpha,
                breast_laterality
            ] = alpha_theta_calculator(med_tan_gantry, lat_tan_gantry, med_tan_Y2, lat_tan_Y2)

            print(np.rad2deg(med_tan_theta), np.rad2deg(lat_tan_theta), np.rad2deg(med_tan_alpha), np.rad2deg(lat_tan_alpha), breast_laterality)

            med_tan_col = collimator_angle_calculator(med_tan_theta, med_tan_alpha, "med", breast_laterality)
            lat_tan_col = collimator_angle_calculator(lat_tan_theta, lat_tan_alpha, "lat", breast_laterality)
            med_tan_couch = couch_angle_calculator(med_tan_theta, med_tan_alpha, "med", breast_laterality)
            lat_tan_couch = couch_angle_calculator(lat_tan_theta, lat_tan_alpha, "lat", breast_laterality)

            # Report matchline angles
            window['med_tan_col'].update(value=np.round(med_tan_col, 1))
            window['lat_tan_col'].update(value=np.round(lat_tan_col, 1))
            window['med_tan_couch'].update(value=np.round(med_tan_couch, 1))
            window['lat_tan_couch'].update(value=np.round(lat_tan_couch, 1))

if __name__ == "__main__":  # Only runs the following if the program is launched directly from this script
    launcher()