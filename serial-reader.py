import serial
import math
import ezdxf
coords = []
switch_state = 0

def create_dxf_from_coordinates(coords, output_file):
    # Create a new DXF document
    doc = ezdxf.new()

    # Retrieve the modelspace which is where the content goes
    msp = doc.modelspace()

    # Loop through the coordinates and draw lines between them
    for i in range(len(coords) - 1):
        msp.add_line(coords[i], coords[i+1])

    # Save the DXF document to a file
    doc.saveas(output_file)

def polar_to_cartesian(r, theta, x0=0, y0=0):
    """
    Convert polar coordinates (radius, angle) to cartesian coordinates.

    Parameters:
    - r: Radius
    - theta: Angle in degrees
    - x0, y0: Cartesian origin

    Returns:
    - x, y: Cartesian coordinates
    """
    # Convert angle from degrees to radians
    theta_rad = math.radians(theta)

    # Calculate cartesian coordinates
    x = x0 + r * math.cos(theta_rad)
    y = y0 + r * math.sin(theta_rad)

    return x, y

def parse_pos(pos):
    global switch_state
    try:
        elems = pos.split(",")
        encoderA = int(elems[0])
        encoderB = int(elems[1])
        angle_A = encoderA * 360 / 4000
        angle_B = (encoderB * 360 / 4000) + angle_A
        posA = polar_to_cartesian(400, angle_A)
        posB = polar_to_cartesian(400, angle_B, posA[0], posA[1])
        # if switch_state == 0:
            # return
        print("angleA: {}".format(angle_A))
        print("angleB: {}".format(angle_B))
        print("POS: {}".format(posB))
        coords.append(posB)
        switch_state = 0
    except Exception as e:
        if pos == "switch":
            switch_state = 1
        if pos == "release":
            switch_state = 0
        print("bad pos: {}".format(pos))

# Open the serial port
ser = serial.Serial('/dev/ttyACM0', 9600)


pos = ""
try:
    while True:
        # Read a byte from the serial port
        data = ser.read(1)

        # Convert the byte to an integer
        # value = ord(data)
        try:
            pos += data.decode()
            if data == b"\n":
                pos = pos.strip()
                parse_pos(pos)
                pos = ""
        except UnicodeDecodeError:
            print(data)

except KeyboardInterrupt:
    # Close the serial port when the script is terminated
    create_dxf_from_coordinates(coords, "output.dxf")
    ser.close()

