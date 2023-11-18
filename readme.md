# build

/home/johan/bin/arduino-cli compile --fqbn arduino:avr:uno --output-dir=output rotary-reader

# upload

sudo -E /home/johan/bin/arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno rotary-reader


