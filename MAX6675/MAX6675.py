# MAX6675
# Created at 2021-01-29 10:55:26.700073

# import the streams module, it is needed to send data around
import streams
import spi


class MAX6675(spi.Spi):

    def __init__(self, spidrv, cs, clk=5000000):
        spi.Spi.__init__(self, cs, spidrv, clock=clk)

    def readTempC(self):
        # """Return the thermocouple temperature value in degrees celsius."""
        v = self._read16()
        # Check for error reading value.
        if v & 0x4:
            return float('NaN')
        # Check if signed bit is set.
        if v & 0x80000000:
            # Negative value, take 2's compliment. Compute this with subtraction
            # because python is a little odd about handling signed/unsigned.
            v >>= 3  # only need the 12 MSB
            v -= 4096
        else:
            # Positive value, just shift the bits to get the value.
            v >>= 3  # only need the 12 MSB
        # Scale by 0.25 degrees C per bit and return value.
        return v * 0.25

    def _read16(self):
        # Read 16 bits from the SPI bus.
        self.lock()
        self.select()
        raw = self.read(2)
        self.unselect()
        self.unlock()

        if raw is None or len(raw) != 2:
            raw = -1
        value = raw[0] << 8 | raw[1]

        return value


# open the default serial port, the output will be visible in the serial console
streams.serial()

max_6675 = MAX6675(SPI0, D27)

# loop forever
while True:
    temp_6675 = max_6675.readTempC()
    print('temp= ', temp_6675)

    sleep(1000)
