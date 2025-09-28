Here is a curated list of scientific papers, categorized to help you navigate from the foundational concepts to the state-of-the-art.

-----

### 🏛️ 1. Foundational & Seminal Papers

These are the classic papers that established the core principles of the field.

  * **Title:** **[Neuromorphic electronic systems](https://www.google.com/search?q=https://labs.cms.caltech.edu/media/articles/cmead-1990.pdf)**

      * **Authors:** Carver Mead (1990)
      * **Why it's important:** This is the paper that started it all. Mead lays out the philosophical and engineering vision for building electronic systems that mimic the structure and principles of the brain, emphasizing low-power, parallel, and event-driven computation.

  * **Title:** **[A 128x128 120 dB 15 µs Latency Asynchronous Temporal Contrast Vision Sensor](https://www.ifi.uzh.ch/dam/jcr:18928364-d16b-4403-9217-2098aaad72bd/lichtsteiner_dvs_jssc08.pdf)**

      * **Authors:** P. Lichtsteiner, C. Posch, and T. Delbruck (2008)
      * **Why it's important:** This is the landmark paper introducing the first practical, high-performance Dynamic Vision Sensor (DVS), the basis for modern event cameras. It demonstrated the key advantages of asynchronous, sparse event generation for vision.

  * **Title:** **[Synaptic plasticity: timing is everything](https://www.ifi.uzh.ch/dam/jcr:18928364-d16b-4403-9217-2098aaad72bd/lichtsteiner_dvs_jssc08.pdf)**

      * **Authors:** Guo-qiang Bi and Mu-ming Poo (1998)
      * **Why it's important:** This highly influential neuroscience paper experimentally established Spike-Timing-Dependent Plasticity (STDP), a fundamental biological learning rule. STDP has been a major inspiration for learning algorithms in SNNs.

### 🧠 2. Neuromorphic Hardware (Brainchips)

Papers describing the architecture and capabilities of the most prominent neuromorphic chips.

  * **Title:** **[Loihi: A Neuromorphic Manycore Processor with On-Chip Learning](https://www.google.com/search?q=https://www.intel.com/content/dam/www/programmable/us/en/pdfs/literature/conference/icrc/icrc18-davies.pdf)**

      * **Authors:** M. Davies et al. (Intel Labs) (2018)
      * **Why it's important:** The primary paper detailing the architecture of Intel's first-generation neuromorphic research chip, **Loihi**. It explains its asynchronous design, programmable "neuron cores," and on-chip learning capabilities.

  * **Title:** **[A million-spike-per-second silicon neuron for building massively parallel neural networks](https://www.google.com/search?q=https://www.research.manchester.ac.uk/portal/files/54573880/FULL_TEXT.PDF)**

      * **Authors:** S. B. Furber, F. Galluppi, S. Temple, L. A. Plana (2014)
      * **Why it's important:** This paper describes the custom architecture of the **SpiNNaker** system, which is designed for large-scale, real-time simulation of SNNs, making it a crucial tool for both neuroscience and neuromorphic algorithm development.

  * **Title:** **[TrueNorth: A 1 Million Neuron Integrated Circuit with a 4096-Neuron Crossbar per Core](https://www.science.org/doi/10.1126/science.1254642)**

      * **Authors:** P. A. Merolla et al. (IBM Research) (2014)
      * **Why it's important:** Published in *Science*, this paper introduced IBM's **TrueNorth** chip. It was a milestone in demonstrating the scalability and extreme energy efficiency ($~70mW$) of digital neuromorphic hardware for real-time inference.

### ⚡ 3. SNN Training & Algorithms

This is where much of the "hot" research is focused: finding effective ways to train SNNs.

  * **Title:** **[Surrogate Gradient Learning in Spiking Neural Networks](https://arxiv.org/abs/1901.09948)**

      * **Authors:** E. O. Neftci, H. Mostafa, F. Zenke (2019)
      * **Why it's important:** This paper provides a clear and comprehensive overview of the **surrogate gradient** method, which is the key technique that allows SNNs to be trained with backpropagation, just like traditional deep neural networks. It unlocked deep learning-style performance for SNNs. **This is a must-read for anyone serious about SNNs.**

  * **Title:** **[Fast-classifying, high-accuracy spiking deep networks through weight and threshold balancing](https://ieeexplore.ieee.org/document/7552940)**

      * **Authors:** P. U. Diehl et al. (2015)
      * **Why it's important:** A highly cited paper on the **ANN-to-SNN conversion** technique. It shows how to take a pre-trained, high-performance Artificial Neural Network (ANN) and convert it into an SNN that performs the same task with very low latency and high energy efficiency.

### 🚀 4. Modern Applications & State-of-the-Art (SOTA)

These papers show the whole stack in action: event cameras, SNNs, and neuromorphic hardware working together to solve real problems.

  * **Title:** **[Event-based Vision: A Survey](https://arxiv.org/abs/1904.08405)**

      * **Authors:** G. Gallego et al. (2020)
      * **Why it's important:** This is the definitive modern survey of the event-based vision field. It covers everything from sensor physics to state-of-the-art algorithms for feature detection, optical flow, SLAM, and object recognition. It's the best starting point to understand the current landscape.

  * **Title:** **[Opportunities for neuromorphic computing algorithms and applications](https://www.google.com/search?q=https://www.nature.com/articles/s43588-022-00214-7)**

      * **Authors:** C. D. Schuman et al. (2022)
      * **Why it's important:** A recent and forward-looking review published in *Nature Computational Science*. It discusses the current challenges and future opportunities for neuromorphic computing, highlighting where the field is likely to have the most impact, from scientific computing to edge AI.

  * **Title:** **[Live Demonstration: Event-based Neuromorphic System for Gesture Recognition](https://www.google.com/search?q=https://ieeexplore.ieee.org/document/8975932)**

      * **Authors:** I. Ceolini et al. (2019)
      * **Why it's important:** A great example of a full end-to-end system. It uses an event camera to see, a Spiking Convolutional Neural Network (SCNN) to process, and a neuromorphic chip to compute—all for a real-time gesture recognition task. This demonstrates the practical integration of the entire stack.
