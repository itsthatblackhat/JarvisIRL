## Project Overview

JarvisIRL is designed to function as a master neural network, integrating multiple sub-neural networks that correspond to different regions of the brain. Each sub-neural network operates semi-autonomously, handling specific tasks while collaborating with other networks to achieve the overall goals of the system.

### Master Neural Network: Jarvis
Jarvis serves as the central coordinating entity, responsible for high-level decision-making, resource allocation, and overall system management. It integrates the functionalities of various sub-neural networks to create a cohesive and efficient operation.

### Sub-Neural Networks
Each sub-neural network within JarvisIRL represents a distinct region of the brain, with specialized functions and interactions. These networks include:

1. **Basal Ganglia Neural Network**: Handles motor control and learning.
   - `basal_ganglia_neural.py`: Implements the functionalities of the basal ganglia.

2. **Brainstem Neural Network**: Manages basic life functions such as heartbeat and breathing.
   - `brainstem_neural.py`: Contains the logic for brainstem operations.

3. **Cerebellum Neural Network**: Responsible for fine motor control and balance.
   - `cerebellum_neural.py`: Implements cerebellum-specific processes.

4. **Cerebrum Neural Network**: The largest part of the brain, dealing with higher cognitive functions.
   - `cerebrum_neural.py`: Manages complex thought processes, decision-making, and learning.

5. **Hypothalamus Neural Network**: Regulates homeostasis, including temperature, hunger, and thirst.
   - `hypothalamus_neural.py`: Controls autonomic functions and endocrine activity.

6. **Limbic Neural Network**: Associated with emotions, behavior, and long-term memory.
   - `limbic_neural.py`: Handles emotional responses and memory formation.

7. **Reticular Neural Network**: Involved in sleep-wake cycles and consciousness.
   - `reticular_neural.py`: Manages states of alertness and consciousness.

8. **Thalamus Neural Network**: Acts as a relay station, directing sensory and motor signals to the cerebrum.
   - `thalamus_neural.py`: Processes and transmits neural signals to appropriate areas.

## Model Renderer
The `model_renderer.py` script is responsible for rendering the 3D brain model (`Brain.obj`) with added controls for visualization. This script utilizes the `pywavefront` library to load the 3D model and `moderngl` for rendering.

### Controls
- **Rotation**: Allows manual rotation of the brain model using arrow keys.
- **Zoom**: Enables zooming in and out with the `W` and `S` keys.
- **Auto-Rotate**: Toggles automatic rotation of the model with the `R` key.

### Vertex and Fragment Shaders
The rendering process uses vertex and fragment shaders for Phong shading, which enhances the visual realism of the 3D model.

### Overlaying Brain Activity
The primary purpose of the rendering functionality is to overlay brain activity in the form of light paths or dots, indicating the flow and functionality of different sub-neural networks within the master neural network. This visualization helps in understanding and analyzing the interactions and operations of various brain regions in real-time.

## Memory Module
The memory module manages the storage and retrieval of information within JarvisIRL. It includes:
- `memories.json`: Stores the memory data.
- `memory.py`: Implements the core memory functionalities.
- `memory_imprinting.py`: Handles the process of creating and updating memories.
- `memory_utils.py`: Provides utility functions for memory management.
- `__init__.py`: Initializes the memory module.

## Visualization
The visualization module contains scripts for visualizing different aspects of the neural networks and their interactions:
- `activity_visualization.py`: Visualizes brain activity.
- `communication_visualization.py`: Visualizes communication between different neural networks.
- `__init__.py`: Initializes the visualization module.

## Next Steps
1. **Integrate Brain Activity Overlay**: Develop the functionality to overlay brain activity on the 3D model, showing real-time interactions and data flow.
2. **Enhance Sub-Neural Network Functionalities**: Improve the individual sub-neural networks for better performance and accuracy.
3. **Test and Validate**: Conduct comprehensive testing to ensure all components work seamlessly together.
4. **Documentation**: Create detailed documentation for each module and script, including setup instructions and usage guidelines.


Notes For AI continued development of JarvisIRL: 
Directory Structure:

Here is our directory structure:
    ├───BrainModel
    │       Brain.obj
    │
    ├───data
    ├───gui
    ├───memory
    │   │   memories.json
    │   │   memory.py
    │   │   memory_imprinting.py
    │   │   memory_utils.py
    │   │   __init__.py
    │   │
    │   ├───tests
    │
    ├───models
    ├───motor_control
    ├───nlu
    ├───speech_recognition
    ├───subnet
    │   │   __init__.py
    │   │
    │   ├───BasalGangliaNeural
    │   │   │   basal_ganglia_neural.py
    │   │   │
    │   │
    │   ├───BrainstemNeural
    │   │   │   brainstem_neural.py
    │   │   │
    │   │
    │   ├───CerebellumNeural
    │   │   │   cerebellum_neural.py
    │   │   │
    │   │
    │   ├───CerebrumNeural
    │   │   │   cerebrum_neural.py
    │   │   │
    │   │
    │   ├───HypothalamusNeural
    │   │   │   hypothalamus_neural.py
    │   │   │
    │   │
    │   ├───LimbicNeural
    │   │   │   limbic_neural.py
    │   │   │
    │   │
    │   ├───ReticularNeural
    │   │   │   reticular_neural.py
    │   │   │
    │   │
    │   ├───ThalamusNeural
    │   │   │   thalamus_neural.py
    │   │   │
    ├───tests
    ├───visualization
    │   │   activity_visualization.py
    │   │   communication_visualization.py
    │   │   __init__.py


----------------------------------------------------

