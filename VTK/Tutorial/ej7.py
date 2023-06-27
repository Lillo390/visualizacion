import vtk
import numpy as np
import sys


filename = 'c:/Users/danie/OneDrive/Escritorio/Master/Visualizacion/VTK/ej7.py'

# Cargamos el modelo de aorta
reader = vtk.vtkSTLReader()
reader.SetFileName(filename)

##convert polygonal mesh into triangle mesh
tri = vtk.vtkTriangleFilter()
tri.SetInputConnection(reader.GetOutputPort());

amapper = vtk.vtkPolyDataMapper()
amapper.SetInputConnection(tri.GetOutputPort())

aorta = vtk.vtkActor()
aorta.SetMapper(amapper)

#
# Create the Renderer and assign actors to it. A renderer is like a
# viewport. It is part or all of a window on the screen and it is responsible
# for drawing the actors it has.  We also set the background color here.
#
ren1 = vtk.vtkRenderer()
ren1.AddActor(aorta)
ren1.SetViewport(0.0, 0.0, 0.5, 0.5)
ren1.SetBackground(0.1, 0.2, 0.4)

ren2 = vtk.vtkRenderer()
ren2.AddActor(aorta)
ren2.SetBackground(0.1, 0.2, 0.4)
ren2.SetViewport(0.5, 0.0, 1.0, 0.5)


ren3 = vtk.vtkRenderer()
ren3.AddActor(aorta)
ren3.SetBackground(0.1, 0.2, 0.4)
ren3.SetViewport(0.0, 0.5, 0.5, 1.0)


ren4 = vtk.vtkRenderer()
ren4.AddActor(aorta)
ren4.SetBackground(0.1, 0.2, 0.4)
ren4.SetViewport(0.5, 0.5, 1.0, 1.0)

#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300.
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( ren1 )
renWin.AddRenderer( ren2 )
renWin.AddRenderer( ren3 )
renWin.AddRenderer( ren4 )

renWin.SetSize(300, 300)

#
# The vtkRenderWindowInteractor class watches for events (e.g., keypress,
# mouse) in the vtkRenderWindow. These events are translated into
# event invocations that VTK understands (see VTK/Common/vtkCommand.h
# for all events that VTK processes). Then observers of these VTK
# events can process them as appropriate.
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#
# By default the vtkRenderWindowInteractor instantiates an instance
# of vtkInteractorStyle. vtkInteractorStyle translates a set of events
# it observes into operations on the camera, actors, and/or properties
# in the vtkRenderWindow associated with the vtkRenderWinodwInteractor.
# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

#
# Unlike the previous scripts where we performed some operations and then
# exited, here we leave an event loop running. The user can use the mouse
# and keyboard to perform the operations on the scene according to the
# current interaction style.
#

#
# Initialize and start the event loop. Once the render window appears, mouse
# in the window to move the camera. The Start() method executes an event
# loop which listens to user mouse and keyboard events. Note that keypress-e
# exits the event loop. (Look in vtkInteractorStyle.h for a summary of events, or
# the appropriate Doxygen documentation.)
#
iren.Initialize()
iren.Start()
