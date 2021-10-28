# Introduction
This project marks the extent of our effort to classify an image or frame of video feed to be encompassing smoke and fire. The proposed system can potentially replace the additional infrastructure required to detect and alert the inhibitants about the potential threat poised by fire and smoke germinated in the surrounding. The naive way of handling fire safety is through smoke detectors which are esentially sensors that either use photoelectronic method or ionization method to detect the presence of smoke and alert the inhibitants through buzzers. Eventhough these smoke detectors are cheap but they require maintainance on regularized manner so as to ensure that the electronic components responsible for detection are in working condition, apart from this it is quite easy to manipulate these dubious electronics as they do not have any intelligence built into it to distinguish between smoke from burning logs and smoke from fragrant sprints. This is the reason why the modern researchers have proposed usage of machine learning techniques which learns from the human anotated data and easier to tweak such that the false positives can be avaoided as far as possible. 

The solution that we are proposing involves usage of the survellince cameras which are prerequisite these days and thus does not require an additional capital to purchase smoke detectors and bare their maintanance cost i.e. one bullet to shoot two geese. The camera feed will be fed into the ML model which will classify the set/series of frames to be on fire ;-) or not. Based on the classification, frames can be termed to be safe or unsafe and if the frames turns out to be in the unsafe state then an automated warning will be flagged. In the above paragraph, We have turned pages of false positives but we need to understand that it may be incovenient at first hand but it is not as significantly dangerous as true negative. So, the agenda of the classification model is that we need to lower down the true negative rate as low as possible.  

This marks end of our brainstorming. 

# Problem statement
Given frames of video feed or an image construct a machine learning model that can classify it into binary classes viz., safe or unsafe. Unsafe class of images dominantly consists of fire or smoke or potentially both at the same time.

# Proposed solution
The solution involves deep neural network architecture consisting of convolutional neural networks which are best suited for computer vision. Optimization of network parameters is not enough since we are expecting such dynamic domain of images to be fed into our model and thus hyperparameter tuning is mandatorily anticipated. EDA will be used to perfect the architecture of the model which in farther phases can be incorporated as backend API. The finished proect will be a web application equipped with inferencing API. It is not very interesting to classify images which already acheived above par accuracies in acedemic resaerch datasets rather we want out classifier to go one step ahead and localize the bounding box across the flame. The state of the art algorithm that localizes the bounding box coordinates across the region of interest in the images or video frames is YOLO (cool name!).    

# Hardware and Software requirements
	## Hardware requirements
		1. RAM >= 4GB
		2. AVX instruction set archiecture

	## Software requirements
		1. Python 3.6–3.9; Python 3.9 support requires TensorFlow 2.5 or later; Python 3.8 support requires TensorFlow 2.2 or later.
		2. pip 19.0 or later (requires manylinux2010 support)
		3. Ubuntu 16.04 or later (64-bit)
		4. macOS 10.12.6 (Sierra) or later (64-bit) (no GPU support); macOS requires pip 20.3 or later
		5. Windows 7 or later (64-bit) ; Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017 and 2019
		6. GPU support requires a CUDA®-enabled card (Ubuntu and Windows)

