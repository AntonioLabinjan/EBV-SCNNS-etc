-----

## 🌐 General & Overarching Resources

Vrhunski repo: https://github.com/uzh-rpg/event-based_vision_resources


These resources provide a high-level overview and connect the different parts of the brain-inspired computing stack.

  * **Websites & Communities:**

      * **[iniForum](https://www.google.com/search?q=https://forum.ini.uzh.ch/)**: The main community forum for neuromorphic engineering, hosted by the Institute of Neuroinformatics (UZH/ETH Zurich). A great place to ask questions.
      * **[Telluride Neuromorphic Cognition Engineering Workshop](https://www.google.com/search?q=https://telluride.ini.uzh.ch/)**: An annual, influential workshop in the field. The projects and lecture slides from past years are a goldmine of information.

  * **Introductory Videos:**

      * **[The Future of AI: Neuromorphic Computing](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DpiO0424a5I8)** by Intel: A fantastic, high-level introduction to why neuromorphic computing is needed and how it differs from traditional AI.
      * **[Neuromorphic Engineering: An Introduction](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3D__LqA3-iG_o)** by Prof. Giacomo Indiveri: A classic academic lecture that provides a solid foundation for the entire field.

  * **Key Review Papers:**

      * **[Event-based Vision: A Survey](https://arxiv.org/abs/1904.08405)** by Gallego et al.: The definitive guide to event-based vision, covering sensors, data formats, and core algorithms. **This is a must-read.**
      * **[Deep learning with spiking neurons: opportunities and challenges](https://arxiv.org/abs/1812.01304)** by Pfeiffer and Pfeil: A great overview of how SNNs fit into the modern deep learning landscape.

-----

## 👁️ Event-Based Vision

Resources focused on the sensors and data processing for event cameras (Dynamic Vision Sensors - DVS).

  * **Websites & Manufacturers:**

      * **[Prophesee](https://www.prophesee.ai/)**: A leading manufacturer of event-based sensors and software. Their website has excellent application demos.
      * **[iniVation](https://inivation.com/)**: A company spun out of the pioneering UZH/ETH Zurich lab, offering various event cameras.
      * **[RPG - Robotics and Perception Group (UZH)](https://rpg.ifi.uzh.ch/research_dvs.html)**: A key academic lab that publishes cutting-edge research and open-source datasets for drones and robotics using event cameras.

  * **YouTube Videos & Tutorials:**

      * **[How an Event Camera Works](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DLAKk_2c7s5w)**: A clear, concise explanation of the fundamental principles of event cameras versus traditional cameras.
      * **[Event-Based Vision for High-Speed Robotics](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3D1b5P3pI3a_Y)**: A presentation from RPG showing the practical advantages of event cameras in robotics.

  * **Code & Datasets:**

      * **[Tonic - The Event-Based Data Toolkit](https://github.com/neuromorphs/tonic)**: A PyTorch-based library that makes downloading and handling event-based datasets (like N-Caltech101, Prophesee-100, etc.) incredibly simple.
      * **[AEViewer](https://www.google.com/search?q=https://inivation.com/support/software/aeviewer/)**: The "Swiss army knife" for visualizing and recording data from live event cameras.
      * **[The Event Camera Dataset and Simulator](https://rpg.ifi.uzh.ch/davis_data.html)**: A classic dataset for tasks like visual odometry and SLAM with event cameras.

-----

## 🧠 Neuromorphic Computing & Brain-Inspired Chips

Resources related to the specialized hardware designed to run brain-inspired algorithms efficiently.

  * **Websites & Projects:**

      * **[Intel Neuromorphic Computing Lab](https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html)**: The official home for Intel's **Loihi** chip. Contains research updates, publications, and news.
      * **[SpiNNaker Project](https://www.google.com/search?q=https://www.cs.man.ac.uk/spinnaker/)**: The homepage for the SpiNNaker (Spiking Neural Network Architecture) machine at the University of Manchester, a massively parallel system designed to simulate large-scale SNNs in real-time.

  * **YouTube Videos:**

      * **[Steve Furber: SpiNNaker and the Human Brain Project](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DI-S_4-yv8vA)**: A talk from one of the pioneers of the field, explaining the motivation and architecture behind SpiNNaker.
      * **[Intel's Loihi 2](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3Dd_soXy41p2w)**: Intel's official video showcasing the capabilities and advancements of their second-generation neuromorphic research chip.

  * **Software Frameworks for Hardware:**

      * **[Lava Software Framework](https://github.com/lava-nc/lava)**: An open-source, Python-based framework from Intel for developing applications that can run on Loihi and other neuromorphic hardware. **This is the main tool for working with Loihi.**

-----

## ⚡ Spiking Neural Networks (SNNs)

Resources for the algorithms and software frameworks used to build and train SNNs.

  * **Tutorials & Courses:**

      * **[snnTorch Tutorial Series](https://snntorch.readthedocs.io/en/latest/tutorials/index.html)**: **The best starting point for beginners.** This PyTorch-based library has outstanding documentation and step-by-step tutorials that cover everything from the basics of leaky-integrate-and-fire (LIF) neurons to advanced training techniques like surrogate gradients.
      * **[Neuromatch Academy](https://neuromatch.io/)**: An online computational neuroscience course. While not strictly focused on SNNs for AI, its content provides a deep understanding of the neural dynamics that SNNs are based on.

  * **Code Examples & Libraries:**

      * **[snnTorch (GitHub)](https://github.com/jeshraghian/snntorch)**: A user-friendly PyTorch library for SNNs. Excellent for rapid prototyping and deep learning-style training.
      * **[Norse (GitHub)](https://github.com/norse/norse)**: Another solid PyTorch-based library for SNNs, focused on bio-inspired learning.
      * **[Brian2](https://briansimulator.org/)**: A Python simulator for SNNs that is more focused on biological realism and computational neuroscience research than machine learning applications.

  * **Key Papers on SNN Training:**

      * **[Surrogate Gradient Learning in Spiking Neural Networks](https://arxiv.org/abs/1901.09948)** by Neftci et al.: A foundational paper explaining the most popular and effective method for training deep SNNs using tools from traditional deep learning (i.e., backpropagation).


Cool video
https://youtu.be/2tLGNFlS7bM?si=5LXCnkSnPfBkDMV5

Resursi iz papera: (OBAVEZNO SVE ISTRAŽIT I ISPROBAT :D )
- za sad još nema neke standard biblioteke integrirane u OpenCV koja upotrebljava EBV
- jAER - Java-based enviroment za event senzore i procesiranje (noise reduction, feature extraction, optical flow, de-rotation (IMU, CNN, RNN)
- pomoću jAER su napravljeni brojni ne-mobilni roboti; ima i mobilnih, ali jAER nije idealan za to)
- libcaer - C biblioteka za konfiguraciju i obradu podataka iz iniVation i aiCTX neuromorfnih senzora i procesora (DVS i DAVIS kamere + Dynap-SE neuromorfni procesor)
- ROC DVS paket - temeljen na libcaeru; C++ driveri za DVS i DAVIS (super za robotiku jer se lako integrira s robotskim OS-ovima)
- event-driven YARP - libraries za rad s neuromorphic senzorima + algoritmima za procesiranje event podataka (YARP = yet another robot platform)
- pyAER - python wrapper napravljen oko libcaera -> ima puno poetencijala...forši to istražit
- DV - C++ open-source softver za iniViation DVS/DAVIS -> službeni SDK za to

DATASETS & SIMULATORS
Ima dobrih dataseta za: target motion estimation, image reconstruction (regresija), target recognition (klasifikacija)
Regresija -> optical flow, SLAM, object tracking, segmetation
Klasifikacija -> object and action recognition
