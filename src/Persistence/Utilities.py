import numpy as np
from copy import deepcopy

def pianoAugmentation(npArray):

    pianos = []
    piano_fliplr = np.fliplr(npArray) # axis Y
    piano_flipud = np.flipud(npArray) # axis X

    pianos.append(npArray)
    pianos.append(piano_fliplr)
    pianos.append(piano_flipud)

    col2search = np.argmax(np.max(npArray, 1))
    piano_fliplr_ind = np.argmax(piano_fliplr[col2search,:])
    npArray_ind = np.argmax(npArray[col2search,:])

    down = deepcopy(piano_fliplr)
    up = deepcopy(npArray)

    # modifiying octaves
    while piano_fliplr_ind>npArray_ind:
        down = np.roll(down, -11, axis=1)
        up = np.roll(up, 11, axis=1)
        piano_fliplr_ind = np.argmax(down[col2search,:])
        npArray_ind = np.argmax(up[col2search,:])

        pianos.append(down)
        pianos.append(up)

    return(pianos)