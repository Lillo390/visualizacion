
from __future__ import print_function
import vtk
import time

#
# define the callback
#
def myCallback(obj,string):
    print("Starting a render")


#
# create the basic pipeline as in Step1
#
cone = vtk.vtkConeSource()
cone.SetHeight( 3.0 )
cone.SetRadius( 1.0 )
cone.SetResolution( 10 )

coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection( cone.GetOutputPort() )
coneActor = vtk.vtkActor()
coneActor.SetMapper( coneMapper )

ren1= vtk.vtkRenderer()
ren1.AddActor( coneActor )
ren1.SetBackground( 0.1, 0.2, 0.4 )

#
# Add the observer here
#
ren1.AddObserver("StartEvent", myCallback)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( ren1 )
renWin.SetSize( 300, 300 )

#
# now we loop over 360 degrees and render the cone each time
#
for i in range(0,360):
    time.sleep(0.03)
    renWin.Render()
    
ren1.GetActiveCamera().Azimuth( 1 )
