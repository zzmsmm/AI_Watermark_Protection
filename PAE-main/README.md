# PAE
This repository contains one implementation of the model presented in the manuscript 

"PERSISTENT WATERMARK FOR IMAGE CLASSIFICATION NEURAL NETWORKS BY PENETRATING THE AUTOENCODER", 

submitted to IEEE International Conference on Image Processing 2021 (ICIP2021).

The proposed model generates persistent backdoor into deep neural networks (especially those for image processing) as an identification of the author's identity.

Backdoor has been widely adopted as the authorship identification for black-box deep model watermarks. 

However, naive backdoors can be easily invalidated by adding an autoencoder in the front of the plagiarized model. 

This paper introduces one method of generating persistent watermark by penetrating the autoencoder (w.r.t. a dataset). 

The idea is to approximate the autoencoder used by the adversary with a collection of shadow autoencoders trained locally.

For details, see the annotations in np2.py.

Dependency: PyTorch, cuda device if avilable.
