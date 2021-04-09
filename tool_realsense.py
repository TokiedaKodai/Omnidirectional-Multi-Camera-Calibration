import usb

import config as cf


def reset_usb():
    def is_realsense_device(dev):
        is_same_idVendor = dev.idVendor == cf.ID_VENDOR_REALSENSE
        if not is_same_idVendor:
            return False

        is_same_manufacturer = cf.MANUFACTURER_REALSENSE in dev.manufacturer
        is_same_product = cf.PRODUCT_REALSENSE in dev.product

        return is_same_manufacturer and is_same_product

    usb_devices = usb.core.find(find_all=True)
    realsense_devices = list(filter(is_realsense_device, usb_devices))
    print(realsense_devices)

    for dev in realsense_devices:
        print("reset RealSense devices:", dev)
        dev.reset()