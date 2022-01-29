import matplotlib.pylab as plt
from PIL import Image
from numba import jit

@jit
def inversion_coordinate(z, x_center, y_center, radius):

    if(z.real != x_center or z.imag != y_center):
        new_real = x_center + radius**2*(z.real - x_center)/((z.real - x_center)**2 + (z.imag - y_center)**2)
        new_imag = y_center + radius**2*(z.imag - y_center)/((z.real - x_center)**2 + (z.imag - y_center)**2)

    else:
        new_real = x_center
        new_imag = y_center

    new_z = complex(new_real,new_imag)

    return new_z

@jit
def inversion(res, img, wigth, higth, radius, x_center, y_center):
    for x in range(wigth):
        for y in range(higth):
            z = complex(x, y)
            Z = inversion_coordinate(z, x_center, y_center, radius)
            
            if (int(Z.real) <= wigth and int(Z.imag) <= higth):
                if ((x - x_center)**2 + (y - y_center)**2 > radius**2):
                    res[x,y] = img[int(Z.real), int(Z.imag)]
                    res[int(Z.real), int(Z.imag)] = img[x,y]
            else:
                continue
    return res

def main():
    img = plt.imread(r'C:\\Users\\HONOR\\Desktop\\Дима\\Программирвоание\\Инверсия\\Пейзаж.jpg')
    res = img.copy()
    wigth = res.shape[0]
    higth = res.shape[1]
    res = inversion(res, img, wigth, higth, 200, wigth/2, higth/2)

    new_image = Image.fromarray(res)
    new_image.save("Детализирвоанное_фото_v2_r.jpg")

    file = Image.open('Детализирвоанное_фото_v2_r.jpg')
    file.show()

if __name__ == "__main__":
    main()
