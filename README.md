# Project JarvisIRL

## Overview
JarvisIRL is an artificial intelligence project aimed at creating a virtual assistant inspired by the concept of a human brain. The project utilizes neural network architecture to simulate various brain regions, each responsible for different functions such as processing sensory input, decision-making, memory storage, and action execution.

## Features
- **Modular Architecture**: JarvisIRL is designed with a modular architecture, where different brain regions are represented as individual neural networks, allowing for easy scalability and customization.
- **Memory Interaction**: The project incorporates a memory module that stores and retrieves past experiences, enabling the virtual assistant to learn and adapt over time.
- **User Interaction**: JarvisIRL interacts with users through various input methods such as voice commands, text queries, and sensor data.
- **Decision-Making**: Based on user input and past experiences stored in memory, JarvisIRL makes decisions to perform specific actions or provide relevant responses.
- **Error Handling and Safety**: The virtual assistant implements mechanisms for error handling and ensuring safety, minimizing the risk of harmful actions.

( NOTE: run the testmod file to generate the .txt from the 3MF if you are using your own 3MF model )
## Installation
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/itsthatblackhat/JarvisIRL.git
   ```
2. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Navigate to the project directory:
   ```
   cd JarvisIRL
   ```
2. Run the `master.py` file to start the JarvisIRL virtual assistant:
   ```
   python master.py
   ```
3. Follow the on-screen prompts to interact with JarvisIRL.

## Project Structure
The project directory structure is organized as follows:
```
JarvisIRL/
│
├── cerebellum_neural.py        # Implementation of the Cerebellum neural network
├── cerebrum_neural.py          # Implementation of the Cerebrum neural network
├── brainstem_neural.py         # Implementation of the Brainstem neural network
├── thalamus_neural.py          # Implementation of the Thalamus neural network
├── hypothalamus_neural.py      # Implementation of the Hypothalamus neural network
├── basal_ganglia_neural.py     # Implementation of the Basal Ganglia neural network
├── limbic_neural.py            # Implementation of the Limbic neural network
├── reticular_neural.py         # Implementation of the Reticular neural network
│
├── master.py                   # Main file containing the MasterNeural class
├── memory.py                   # Implementation of the Memory class
├── memory_imprinting.py        # Implementation of the MemoryImprinting class
├── subnet.py                   # Subnet module containing neural network classes
├── visualization/             # Directory containing visualization modules
│   ├── communication_visualization.py   # Implementation of CommunicationVisualization class
│   ├── activity_visualization.py        # Implementation of ActivityVisualization class
│
├── requirements.txt            # List of project dependencies
└── README.md                   # Project README file
```

## Contributing
Contributions to JarvisIRL are welcome! If you have any suggestions, bug fixes, or new features to propose, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
