## Steps to reproduce

### Creating the spectrograph

All necessary files are included in the [cad directory](cad/). The cad files are agnostic to specific 3D printers, however
the original print was done with a Bambu Labs printer. Ideally, you should plan to include some kind of surface to which
you can mount the mounting bracket to, as it ensures that the spectrograph stays still. For the original design, this was a 
small sheet of plywood.

After printing at least the top and bottom plates, it is advised to first pre-install all necessary M3 screws using form tapping
to create the threads in the plastic. This step makes it much easier to assemble once the optical compenents are in place.

Place the transmissive grating and optical elements into the respective slots. Note that orientation matters for the collimating
and focus lenses. Ensure that both lenses have the round edge facing the transmissive grating. It can be useful to use small pieces
of foam or filler to ensure a snug fit for the lenses and grating. Try to ensure that each element is centered in the optical train.
Attach the 2 razors on the inside of the front plate, oriented such that you can just barely see light passing through. Make sure 
that both razors are parallel to each other. Then use the short M3 screws and nuts to secure each razor in place.

Once all of the elements are secured in the bottom plate, attach the top plate using the pre-threaded M3 screw holes. Ensure that
the light-trap guards are overlapping around the full spectrograph to ensure no light-leakage. 

Finally, insert the camera using a 1.25" T mount adapter and use 2 M3 thumbscrews to secure it in place. Optionally, you can 
now mount the whole system to the mounting bracket.

### Obtaining Calibration Data 

To create properly reduced final data, you need to have the following sets of frames:

- Light Frames (your actual data)
- Bias Frames (zero second exposures that capture small flaws in the camera sensor)
- Dark Frames (exposures where no light is allowed to come in to identify bias within the camera's own heat signature)
- Flat Frames (an evenly illuminated light source to detect local differences along the sensor)

Obtaining bias frames is trivial with most acquisition software. This project used the free tier of SharpCap imaging software,
which includes functionality for bias frame acquisition. Dark frames can be obtained by simply covering the imaging train with 
a blanket or other object to ensure that no light gets in, then taking exposures at the same intervals of the Light Frames.

For the Flat frames, I used the spectra of a tungsten bulb lamp taken through the spectrograph to act as a standardized blackbody 
emission. This was done by simply pointing the spectrograph at a powered tungsten lamp, then tkaing a series of images such that the
mean pixel value was about half-max, or around 30,000-40,000 pixel value with a 16bit sensor. 

Additionally, for spectral calibration it is required to have a standard emitter. For this project, an Argon lamp was used to 
identify the known peaks and calibrate the pixel-to-wavelength relationship.

### Obtaining Light Frames 

Once you have all necessary calibration data, you can image the desired target spectra. An example was done with an old-fashioned
magnesium flash bulb. For time-series analysis, consider taking images in continuous mode at frequent intervals to capture the spectra 
against time. 

Note that it is helpful to use a dark room when imaging, allowing for minimal external light to leak into the system and blur out 
the source signal. 

### Reducing the Data 

#### Creating Master Calibration Frames 

The standard approach for image reduction is to use multiple of each type of calibration frame and average the pixel values into 
one "Master" frame for each frame type. This is easily done in software like AstroImageJ, which has it's own data reduction pipeline.
I highly recommend following a walkthrough guide on astronomical image reduction, as this project uses the same steps. This guide will 
assume that you have a set of Master Darks, Flats, and Bias frames at this point and have fully reduced all Light frames.

#### Plotting Light frames 

To visualize the FITS image data as a 2d plot, this project uses a simple [python script](analysis/spectral_to_csv.py) to average 
the central 20 rows of pixels into a 1d csv array. This allows for easy plotting of pixel column v. Intensity. More sophisticated 
methods are welcomed, but not necessary due to the target resolution of this design. Whatever method you choose, ensure that you 
have a set of 1d arrays for both the calibration sample data (such as an argon emission), and the actual light frames (such as the flash bulb emissions). 

#### Calibrating wavelenghts 

In this project, the pixel-to-wavelength conversion was done manually through plotting and selecting emission lines on the calibration 
data (argon emission), and comparing to known emission lines. A simple polynomial fit was then found and used to convert the pixel counts. 
This process was not perfect, and more sophisticated methods are available through python packages and other mediums.


