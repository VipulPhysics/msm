import numpy as np
import cv2
import matplotlib.pyplot as plt


# Function to perform unmixing
def unmix_m_vca_sm(image_m, n_components):
    """
    Performs VCA-based unmixing on the input multispectral data.
    """
    # Reshape image dimensions for computation
    if len(image_m.shape) == 4:
        Nw, Ns, Npx, Npy = image_m.shape
    elif len(image_m.shape) == 3:
        Nw, Npx, Npy = image_m.shape
        Ns = 1
        image_m = image_m.reshape((Nw, Ns, Npx, Npy))
    
    image_m2 = image_m.reshape(Nw, -1)
    image_m3 = image_m2.T

    # VCA algorithm
    mat_aux = np.zeros((Nw, Nw))
    mat_aux[:, 0] = np.ones(Nw) / np.sqrt(Nw)

    maximo = []
    for kk in range(n_components):
        w = np.random.randn(Nw)
        f_aux = (np.eye(Nw) - mat_aux @ np.linalg.pinv(mat_aux)) @ w
        f = f_aux / np.linalg.norm(f_aux)
        proj = image_m3 @ f
        pos_max = np.argmax(np.abs(proj))
        max_val = proj[pos_max]
        maximo.append(max_val)
        value_aux = image_m3[pos_max, :]
        mat_aux[:, kk] = value_aux / np.linalg.norm(value_aux)

    A = mat_aux[:, :n_components]
    W = maximo
    S = A
    pinv_s = np.linalg.pinv(S)
    umx_aux = pinv_s @ image_m2
    umx = umx_aux.reshape((n_components, Ns, Npx, Npy))

    return umx, A, W


# Load images
raw_data1 = cv2.imread('red.bmp')
raw_data2 = cv2.imread('green.bmp')
raw_data3 = cv2.imread('blue.bmp')

# Convert images to grayscale
x1 = cv2.cvtColor(raw_data1, cv2.COLOR_BGR2GRAY)
x2 = cv2.cvtColor(raw_data2, cv2.COLOR_BGR2GRAY)
x3 = cv2.cvtColor(raw_data3, cv2.COLOR_BGR2GRAY)

# Create MSP image matrix
xt = np.stack([x1, x2, x3], axis=0)
xd = xt.astype(np.float64) / 255.0  # Normalize to [0, 1]

# Perform unmixing
umx, A, W = unmix_m_vca_sm(xd, 2)
umxd = np.transpose(umx, (2, 3, 0, 1))

# Visualize results
plt.figure()
plt.imshow(-umxd[:, :, 0], cmap='jet')
plt.axis('off')
plt.colorbar()
plt.show()

plt.figure()
plt.imshow(-umxd[:, :, 1], cmap='jet')
plt.axis('off')
plt.colorbar()
plt.show()

plt.figure()
plt.imshow((umxd[:, :, 0] - umxd[:, :, 1]) / 2, cmap='jet')
plt.axis('off')
plt.colorbar()
plt.show()

plt.figure()
plt.plot(A)
plt.show()
