# CUDAEBL
Simulation for eBeam Lithography using Casino3, Python, CUDA and FFT.
The method used for this example purpose uses FFT convolution for exposing pattern and FFT deconvolution to find the dose distribution.

The experimental was performed at 30 kV on a SEM Zeiss Supra 40 equiped with the Raith Elphy Plus electronic pattern generator module.

The simulation uses the Point Spread Function (PSF) simulated by free Casino3 software.

<center>
<img src="phc3dimage.png" style="width:100%;"/>
</center>

The method is not new, it has been reported in the past but with 1D data array. However opensource code is still not available, here the author "reinvent" by using modern hardware to get ride of time consuming and very large data size. Note that unlimited data size method is "inspired" by astrophysical applications that extract very weak and noisy signal.

# Introduction
To write a pattern on a sample coated with a electron sensitive resist, the focused electron beam (ebeam)  (i.e. produced by a Scanning Electron Microscope (SEM)) impingles 'dot by dot' on the surface of the sample. The interaction physic is complex, at the impingled point and around it the resist absorbs a quantity of energy given by a Point Spread function (PSF). The extend area of this absoption depends on the electron range given by the interaction of the beam and the sample. If two dots are close enough each other then the resulting ebeam exposure will be a line or even a surface, that could lead to an unattended pattern.

If you want you expose a simple surface it will be fine but if you want for instance expose two surfaces with a very small gap in between it could be a problem.

This simulation can help you to determine the good dose (the dwelltime of the ebeam at each dot) for your desired pattern. You can visualize the result in 2D with matplotlib or 3D with openGL.

Thanks to the free Casino3 software you can obtain the PSF with the depth of your resist, with any ebeam parameters and any sample and resist. Of course you have to know the parameters of your instrument (the semi-angle of the SEM, the speed of the electronique module, the physical proprieties of your sample, etc.)

Once you get the PSF, this python notebook will help you to do the rest.

You can explore more possibilities: you can mixte two exposures (one at low 5 kV for fast writing a large surface and one at high kV for fine structures). Or you can develop your own algo... and maybe share.

# Requirement:
- Some basic knowledges of python language and jupyter notebook
- Windows 10 64 bits or Linux 64 bits
- 4 Go CPU-RAM (8 recommanded but the more the better)
- A NVIDIA graphic card with at least 2 Go GPU-RAM (the more the better) and cuda capable, check your GPU CUDA-capable here: https://developer.nvidia.com/cuda-gpus

If you have only an old computer and wanna up to 16 Tesla V100 GPU for some bucks you can use Amazon Web Services (aws). The instructions for launching an aws AMI are given in the aws folder.
# Installation
This work was tested on Windows 10, Ubuntu 18.04 on local and on aws EC2 p3.2xlarge. On linux system you can get more GPU RAM available than on Windows system (95 % instead of 81%).
## Casino3
There are many way to obtain the PSF but the easiest way is using Monte Carlo simulation. You can get the PSF from the free software CASINO3 here:http://www.gel.usherbrooke.ca/casino/
Unfortunatley Casino3 is a windows software but you can use Wine in Ubuntu to execute it.
## CUDA toolkit and NVIDIA driver
Download and install CUDA toolkit for your system here: https://developer.nvidia.com/cuda-downloads
The CUDA toolkit file is packed with a display driver.
Installation on Windows 10 is straight forward. In Ubuntu you may to blacklist the default 'nouveau' driver:
### On Ubuntu 18.04
Hereafter are instructions for a fresh Ubuntu install and cudatoolkit version 10.1. Open a Terminal (ctrl+alt+t)
#### 1) update your Ubuntu and install build-essential:
 - sudo apt update
 - sudo apt upgrade
 - sudo apt install build-essential
#### 2) blacklist 'nouveau' driver:
##### 2-a) create file in ~/ folder:
 - cd ~/
 - gedit blacklist-nouveau.conf
##### 2-b) add these two lines and save:
 - blacklist nouveau
 - options nouveau modeset=0
#### 3) remove all previous cuda:
 - sudo apt-get purge nvidia-cuda*
#### 4) logout GUI interface:
 - sudo telinit 3
 - press ctrl+alt+F1 and enter your username and pwd
#### 5) go into super user mode and copy the file you created:
 - sudo -i
 - sudo cp /home/<yourusername>/blacklist-nouveau.conf /etc/modprobe.d
  
#### 6) run:
 - update-initramfs -u
 - exit
 - sudo reboot
#### 7) open a Terminal and cd to the folder where the CUDA toolkit is saved and run:
 - sudo sh cuda_10.1.105_418.39_linux.run
 - then follow instructions (check that the driver installation option is ticked)
 - you can take a coffee...
#### 8) test your installation:
##### 8-1) add cuda PATH:
 - export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}
##### 8-2) run:
 - nvcc -V
 - if you get no error that means your cudatoolkit installation is fine.
#### 9) now reboot Ubuntu and add cuda PATH to your system path. In a Terminal:
 - sudo gedit ~/.bashrc
 - add the two following lines to the end of the file:
   - export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}
   - export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
 - save the file and exit
 - run 'source ~/.bashrc'
 - run again: 'nvcc -V' if no error returned that's fine!

## Anaconda
You can download and install Anaconda for python 3.7 package here : https://www.anaconda.com/distribution/#download-section
Again the installation in Windows is straight forward. In Ubuntu just run this command in a Terminal: 'bash Anaconda3-2019.03-Linux-x86_64.sh' and reboot.

## Dependancies
once Anaconda installed on you system, open a Terminal:
 - cd anaconda
 - anaconda-navigator
1) create a new environment 'cudaenv' with **python 3.6** (due to pyculib package conflicts)
2) in the listBox select 'Not installed' and type 'numpy' in the searchBox then check the checkBox of 'numpy'.
3) do the same as 2) for: scipy, matplotlib, ipython, jupyter, pandas, sympy, nose, pytest, cudatoolkit, pyculib, imageio, pyqtgraph, pyopengl
4) apply and accept for download and installation. Then you can go out and play with your dog...
5) install a specific version 1.16.2 or later for numpy:
  now in the listBox select 'Installed' and search for 'numpy'.
  right-click on the checkBox of 'numpy' and select 'Mark for specific version installation' then select the latest version (1.16.2 or newer)
6) in anaconda-navigator, start a Terminal with your 'cudaenv' and enter 'pip install pycuda'
7) install scikit-cuda with 'pip install scikit-cuda'

# TODO list
- Calibration process using Raith dots pattern and ImageJ software
- Some suggestions to get target exposure data (higher kV PSF, smoothing by convolution separate, etc.)
- Some suggestions to eliminate negative doses
- Some suggestions to overcome large data size when implement dose distribution into hardware
- FFT on very large data (no limit)
- Using aws with preinstalled AMI

# Contributing

If you want to get involved, you are welcome!
