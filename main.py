import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import structlog


logger = structlog.get_logger()

def on_integrate_button_click(event):
    logger.info("Button click")

def main():
    # Configure the serial connection
    SERIAL_PORT = '/dev/cu.usbserial-0001'  # Change this to your serial port
    BAUD_RATE = 921600

    # Open the serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

    # set integration time
    ser.write(b'\xB1')  # Set integration time to 10us

    # Prepare data storage
    NUM_POINTS = 3647
    DATA_SIZE = 7296
    spectral_data: list[int] = [0 for _ in range(NUM_POINTS)]

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(spectral_data)
    ax.set_ylim(0, 6000)
    ax.set_xlim(0, NUM_POINTS)
    ax.set_title('Intensity Data')
    ax.set_xlabel('Point')
    ax.set_ylabel('Intensity')

    try:
        while True:
            spectral_data.clear()

            # Send the request byte
            ser.write(b'\xA1')
            time.sleep(0.05)
            
            # Read the intensity data
            data: bytes = ser.read(DATA_SIZE)
            logger.info(f"Got {len(data)} bytes of data")
            for i in range(1, 3648):
                spectral_data.append(data[2 * i + 1] * 256 + data[2 * i])

            # Update the plot
            line.set_ydata(spectral_data)
            fig.canvas.draw()
            fig.canvas.flush_events()

    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        logger.exception(e)
    finally:
        # Close the serial connection
        ser.close()


if __name__ == "__main__":
    main()
