import os
from OpenSSL import crypto
import usb

usb_serial_number = '0A7205079090'
print("Expected serial number:", usb_serial_number)

# Iterate over all connected USB devices
for device in usb.core.find(find_all=True):
    # Get the serial number of the USB device
    serial_number = device.serial_number
    print("Serial:", serial_number)
    if serial_number == usb_serial_number:
        # Get the device file associated with the USB device
        device_file = usb.util.get_string(device, device.iSerialNumber)
        print("Device:", device_file)
        # Search for the certificate file in the root directory of the USB stick
        for root, dirs, files in os.walk(device_file):
            for file in files:
                print("File name:", file)
                if file.endswith(".pem"):
                    key_file = os.path.join(root, file)
                    break
        break

if key_file and os.path.exists(key_file):
    with open(key_file, 'rb') as f:
        cert_data = f.read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
    store = crypto.X509Store()
    store.add_cert(cert)
    store_ctx = crypto.X509StoreContext(store, cert)
    # Verify the certificate using the store
    if store_ctx.verify_certificate() == None:
        print("Certificate is valid")
        # Allow the software to run
    else:
        # The certificate is not valid, prevent the software from running
        print("Invalid certificate")
else:
    print("Certificate not found on USB stick")
