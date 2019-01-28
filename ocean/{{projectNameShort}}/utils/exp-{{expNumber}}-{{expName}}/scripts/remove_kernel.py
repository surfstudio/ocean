import os


def remove_kernel():
    folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).split('/')[-1]
    s = 'jupyter kernelspec uninstall "{0}" -f'.format(folder)
    os.system(s)

if __name__ == "__main__":
    remove_kernel()
