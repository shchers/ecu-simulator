# ECU Simulator

Author: 2019 Sergey Shcherbakov <shchers@gmail.com>

## Preparing environment

### Prerequisits

  * OS: Linux Debian/Ubuntu, tested on Ubuntu/Kubuntu 16.04+
  * HW: any SocketCAN compatible module

### Preparing host environment

  * Update packages cache
```
sudo apt update
```

  * Install mandatory packages
```
sudo apt install python3 python3-pip
```

  * Install Python CAN module
```
sudo pip3 install python-can
```

  * Download simulator software
```
git clone https://github.com/shchers/ecu-simulator.git
```

  * Connect/enable CAN module

## Running test

  * Configure CAN interface. Pay attention that according to standard you can run at __250 or 500 kbps__

  * Connect OBD-II probe to CAN interface

  * Go to script
```
cd ecu-simulator
```

  * Run script
```
puthon3 ecu-simulator.py
```
