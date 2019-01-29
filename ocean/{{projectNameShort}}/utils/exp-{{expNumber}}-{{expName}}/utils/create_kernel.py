import os


def create_kernel():
    folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).split('/')[-1]
    s = 'python -m ipykernel install --user --name "{0}" --display-name "Python ({0})"'.format(folder)
    os.system(s)

if __name__ == "__main__":
    create_kernel()
