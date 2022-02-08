# IBLabAnalysis

## Automating through an application/ GUI
 
Since most of the plots tend to be repetitive while analyzing the experiments
automating the entire process was necessary. An application was created with this
in mind. This can be useful for everyone since it not only automates the process
and makes it much faster the availability of a GUI allows non programmers to use
it.

## Upload
- On this page we can upload from any of the available tables. It imports all
the data and recognises the experiment.
- Compute deaths computes the parts of the trajectories where the cell dies.
This is a time consuming step so it is helpful to find right at the beginning
so that the remaining steps are almost instantaneous.

<p align="center">
<img src="https://user-images.githubusercontent.com/20139786/152920558-dde6172d-2097-4e4b-9d4d-1c02c296cd8e.png" alt="upload" width="600"/>
</p>

## Average
- The cell trajectories can be viewed in this section. The trajectory range can
be specified and all trajectories within this range can be viewed.
- The mean and standard deviation can be added to the plot for each parameter. This gives a broad perspective of how the mean changes in various conditions.

<p align="center">
<img src="https://user-images.githubusercontent.com/20139786/152920583-9a0cae16-ac5d-4b0e-aa21-1f3add107165.png" alt="average" width="600"/>
</p>

## Phase
- The phase plots help us find out how the parameters keep changing throughout the cell cycle

<p align="center">
<img src="https://user-images.githubusercontent.com/20139786/152920595-e4649887-dddd-4c5e-ba73-2f4ef14bb5e8.png" alt="phase" width="600"/>
</p>

## Contour
- The contour plot shows how the cell contours evolve through time.
- The area plot corresponding to the contours is also shown to give better
understanding of cell shape and size evolution.
- The trajectory can be changed and the video changes dynamically depending
on the input value of cell trajectory
  
<p align="center">
<img src="https://user-images.githubusercontent.com/20139786/152920613-d4d04b1c-7a74-4b09-a6c7-b81e079b1183.png" alt="contour" width="600"/>
</p>
