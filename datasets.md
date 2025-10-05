-----

### 🛠️ Data Handling & Toolkits

Before diving into the datasets, the most important resource you should know about is **Tonic**. It's a PyTorch-based toolkit that handles downloading, parsing, and transforming event-based data for you, much like `torchvision`. It simplifies the process immensely.

  * **[Tonic - The Event-Based Data Toolkit](https://github.com/neuromorphs/tonic)**: Integrates dozens of event-based datasets into a common, easy-to-use framework. **Start here if you want to write code.**

-----

### 🖼️ 1. Image Classification & Object Recognition

These are the "MNIST" and "CIFAR" equivalents for the neuromorphic world. They are excellent for learning the basics of SNNs and event-based data processing.

  * **[N-MNIST & F-MNIST](https://www.garrickorchard.com/datasets/n-mnist)**

      * **Description:** These are neuromorphic versions of the original MNIST (handwritten digits) and Fashion-MNIST datasets. Instead of static images, they consist of recordings of an event camera moving its gaze over an LCD screen displaying the original images.
      * **Use Case:** The "hello world" for SNNs. Perfect for benchmarking simple classification models.

  * **[N-Caltech101](https://www.garrickorchard.com/datasets/n-caltech101)**

      * **Description:** A more complex classification dataset, based on the Caltech101 image set. It was created using the same method as N-MNIST. It contains 101 object categories.
      * **Use Case:** A good step up from N-MNIST for testing more robust object recognition models.

  * **[CIFAR10-DVS](https://www.google.com/search?q=https://figshare.com/articles/dataset/CIFAR10-DVS_a_neuromorphic_dataset_for_object_classification/4724671)**

      * **Description:** A neuromorphic version of the classic CIFAR-10 dataset. It contains recordings of 10,000 images across 10 classes (airplanes, cars, birds, etc.).
      * **Use Case:** A challenging, noisy, and more realistic color image classification benchmark.

-----

### 🚗 2. Autonomous Driving & Robotics

These datasets are larger, more complex, and recorded in real-world environments. They are essential for research in robotics, SLAM (Simultaneous Localization and Mapping), and autonomous vehicles.

  * **[The Multi-Vehicle Stereo Event Camera Dataset (MVSEC)](https://daniilidis-group.github.io/mvsec/)**

      * **Description:** An extensive dataset for autonomous driving and drone navigation. It features data from various sensors, including stereo event cameras, traditional cameras, LiDAR, and IMU, all recorded on cars, drones, and handheld devices in diverse outdoor and indoor environments.
      * **Use Case:** State-of-the-art research in visual odometry, 3D reconstruction, and sensor fusion.

  * **[Event Camera Dataset and Simulator](https://rpg.ifi.uzh.ch/davis_data.html)**

      * **Description:** A foundational dataset from the Robotics and Perception Group (RPG) at the University of Zurich. It contains a wide variety of indoor scenes with high-speed motion, perfect for testing SLAM and visual odometry algorithms. It also comes with a simulator to generate synthetic event data.
      * **Use Case:** Benchmarking high-speed SLAM, visual-inertial odometry, and motion estimation.

  * **[Prophesee GEN1 Automotive Detection Dataset](https://www.google.com/search?q=https://www.prophesee.ai/2020/07/15/automotive-dataset-1-million-objects/)**

      * **Description:** A massive automotive dataset containing over 2000 hours of driving recordings. It features bounding box annotations for over 1 million objects (vehicles, pedestrians), making it the largest event-based dataset for object detection.
      * **Use Case:** Training and evaluating object detectors for automotive applications.

-----

### 👋 3. Gesture & Action Recognition

These datasets focus on high-speed human motion, a task where event cameras naturally excel.

  * **[DVS-Gesture Dataset](https://www.google.com/search?q=https://research.ibm.com/interactive/dvs-gesture/)**

      * **Description:** Contains recordings of 29 different hand and arm gestures under various lighting conditions. It's a widely used benchmark for action recognition.
      * **Use Case:** The standard benchmark for gesture recognition with SNNs and event cameras.

  * **[ASL-DVS (American Sign Language)](https://www.frontiersin.org/articles/10.3389/fnins.2017.00735/full)**

      * **Description:** A large-scale dataset of American Sign Language letters being signed, recorded with an event camera.
      * **Use Case:** More complex and fine-grained gesture recognition, useful for human-computer interaction research.


Upute za caltech dataset
This file is a spiking conversion of the Caltech101 dataset. The conversion process is described in:

Orchard, G.; Cohen, G.; Jayawant, A.; and Thakor, N.  �Converting Static Image Datasets to Spiking Neuromorphic Datasets Using Saccades", Frontiers in Neuromorphic Engineering,  special topic on Benchmarks and Challenges for Neuromorphic Engineering


Each example is a separate binary file (e.g. 'accordion\image_0001.bin') consisting of a list of events. Each event occupies 40 bits arranged as described below:

bit 39 - 32: Xaddress (in pixels)
bit 31 - 24: Yaddress (in pixels)
bit 23: Polarity (0 for OFF, 1 for ON)
bit 22 - 0: Timestamp (in microseconds)

The filenames and directory structure match the original Caltech101 dataset so that spike recordings inlcuded here can be backtraced to the original images.


A Matlab function for "Read_Ndataset.m" is provided for reading these binary files into Matlab, and a Matlab script "RunMe.m" shows how to read data in and use the provided Matlab functions


Additional Matlab functions are available at: http://www.garrickorchard.com/code



Bounding box and object contour annotations are provided for the data, each in a separate file (e.g. 'accordion\annotation_0001.bin'). Each file contains two boundaries. The first is a rectangular box, while the second traces out the object countour. A Matlab script is provided showing how to read the data into Matlab.

For those wishing to write their own functions, the binary values are written as 16bit signed integers

word 0: dimension of points for box (2 because these are 2D images)
word 1: number of points in the box boundary ('N')
word 2: 1st dimension of box point 1
word 3: 2nd dimension of box point 1
word 4: 1st dimension of box point 2
word 5: 2nd dimension of box point 2
.
.
.
word N*2: 1st dimension of box point N
word N*2+1: 2nd dimension of box point N

word N*2+2: dimension of points for contour (2 because these are 2D images)
word N*2+3: number of points in the contour boundary ('M')
word N*2+4: 1st dimension of contour point 1
word N*2+5: 2nd dimension of contour point 1
word N*2+6: 1st dimension of contour point 2
word N*2+7: 2nd dimension of contour point 2
.
.
.
word (N+M+1)*2: 1st dimension of contour point M
word (N+M+1)*2+1: 2nd dimension of contour point M



The bias parameters used by the ATIS during recording are:
APSvrefL:  3050mV
APSvrefH:  3150mV
APSbiasOut: 750mV
APSbiasHyst: 620mV
CtrlbiasLP: 620mV
APSbiasTail: 700mV
CtrlbiasLBBuff: 950mV
TDbiasCas: 2000mV
CtrlbiasDelTD: 400mV
TDbiasDiffOff: 620mV
CtrlbiasSeqDelAPS: 320mV
TDbiasDiffOn: 780mV
CtrlbiasDelAPS: 350mV
TDbiasInv: 880mV
biasSendReqPdY: 850mV
TDbiasFo: 2950mV
biasSendReqPdX: 1150mV
TDbiasDiff: 700mV
CtrlbiasGB: 1050mV
TDbiasBulk: 2680mV
TDbiasReqPuY: 810mV
TDbiasRefr: 2900mV
TDbiasReqPuX: 1240mV
TDbiasPR: 3150mV
APSbiasReqPuY: 1100mV
APSbiasReqPuX: 820mV

