# pyqik

Python class for Pololu Qik motor controllers.
Written for the Qik2s9v1 but Qik2s12v10 should be compatible(not tested)
Website: https://www.pololu.com/category/97/pololu-qik-dual-serial-motor-controllers

These (dual)motor controllers have a serial TTL interface. Use this class to easily use this controller in your python program.

requires: pySerial
http://pyserial.sourceforge.net/

Example usage:
```
 import qik

 qik = qik.Controller()
 qik.setSpeed(0, 0, 50) # motor=0, reverse=0, speed=50
```

