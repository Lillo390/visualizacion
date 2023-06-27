
import numpy as np
import pyvista as pv
import warnings
warnings.filterwarnings("ignore")



pv.set_plot_theme("document")

# download mesh
th = pv.read('./data/thinker.stl')

normals = th.compute_normals()
# Creamos las cuatro ventanas de visualización
p1 = pv.Plotter()
p2 = pv.Plotter()
p3 = pv.Plotter()
p4 = pv.Plotter()


# 1. Visualización del modelo en modo alambre con normales


centers = th.cell_centers().points
arrows = normals['Normals']

p1 = pv.Plotter()
p1.add_text("Alambre con normales", font_size=24)
p1.add_mesh(th, style='wireframe', color='white', show_edges=True)

def arrow_size(val):
    p1.clear_actors()
    p1.add_mesh(th, style='wireframe', color='white', show_edges=True)
    p1.add_arrows(centers, arrows, color='red', mag=val)
    p1.update()

# Añadir slider
slider = p1.add_slider_widget(
    arrow_size,
    [0, 10],  # rango de valores
    title="Tamaño de flechas",
    value=0, pointa=(0.25, 0.1),
    pointb=(0.75, 0.1),style='modern'
)


p1.add_background_image('./data/prado.jpg')
p1.show()
######################################################################################################################

params = [0,False]
decimated_new = th.decimate_boundary(target_reduction=params[0])
p2.add_mesh(decimated_new)

def update_decimate(val):
    params[0]=val
    p2.clear_actors()
    decimated_new = th.decimate_boundary(target_reduction=params[0])
    p2.add_mesh(decimated_new, color=True, show_edges=params[1])
    p2.update()

# Añadir slider
slider_1 = p2.add_slider_widget(
    update_decimate,
    [0, 0.9999],  # rango de valores
    title="Grado de decimado",
    value=0, pointa=(0.25, 0.1),
    pointb=(0.75, 0.1),style='modern'
)
p2.add_background_image('./data/prado.jpg')

def show_edges(val):
    params[1]=val
    p2.clear_actors()
    decimated_new = th.decimate_boundary(target_reduction=params[0])
    p2.add_mesh(decimated_new, color=True, show_edges=params[1])
    p2.update()


p2.add_checkbox_button_widget(show_edges, value=False)

p2.show()


#######################################################################################################################

params = [0,False]
smoothed_new = th.smooth(n_iter=100, relaxation_factor=params[0])
p3.add_mesh(smoothed_new)
p3.add_text("Modelo suavizado", font_size=24)

def update_smoothed(val):
    params[0]=val
    p3.clear_actors()
    smoothed_new = th.smooth(n_iter=100, relaxation_factor=params[0])
    p3.add_mesh(smoothed_new, color=True, show_edges=params[1])
    p3.update()

# Añadir slider
slider_2 = p3.add_slider_widget(
    update_smoothed,
    [0, 0.9999],  # rango de valores
    title="Grado de suavizado",
    value=0,pointa=(0.25, 0.1),
    pointb=(0.75, 0.1),style='modern'
)
p3.add_background_image('./data/prado.jpg')

def show_edges(val):
    params[1]=val
    p3.clear_actors()
    smoothed_new = th.smooth(n_iter=100, relaxation_factor=params[0])
    p3.add_mesh(smoothed_new, color=True, show_edges=params[1])
    p3.update()


p3.add_checkbox_button_widget(show_edges, value=False)

p3.show()

######################################################################################################################
params = [0,0,False]

decimated = th.decimate_boundary(target_reduction=params[0])
graf4 = decimated.smooth(n_iter=100, relaxation_factor=params[1])
p4.add_text("Suavizado y decimado", font_size=24)
p4.add_mesh(graf4, show_edges=params[2], color=True)


def update_decimate(val):
    params[0] = val
    p4.clear_actors()
    decimated = th.decimate_boundary(target_reduction=params[0])
    graf4 = decimated.smooth(n_iter=100, relaxation_factor=params[1])
    p4.add_mesh(graf4, color=True, show_edges=params[2])
    p4.update()

# Añadir slider
slider_3 = p4.add_slider_widget(
    update_decimate,
    [0, 0.9999],  # rango de valores
    title="Grado de decimado",
    value=0,pointa=(0.1, 0.1),
    pointb=(0.5, 0.1),style='modern'
)

def update_smooth(val):
    params[1] = val
    p4.clear_actors()
    decimated = th.decimate_boundary(target_reduction=params[0])
    graf4 = decimated.smooth(n_iter=100, relaxation_factor=params[1])
    p4.add_mesh(graf4, color=True, show_edges=params[2])
    p4.update()

# Añadir slider
slider_4 = p4.add_slider_widget(
    update_smooth,
    [0, 0.9999],  # rango de valores
    title="Grado de suavizado",
    value=0,    pointa=(0.5, 0.1),
    pointb=(0.9, 0.1),style='modern'
)


def show_edges(val):
    params[2]=val
    p4.clear_actors()
    decimated = th.decimate_boundary(target_reduction=params[0])
    graf4 = decimated.smooth(n_iter=100, relaxation_factor=params[1])
    p4.add_mesh(graf4, color=True, show_edges=params[2])
    p4.update()


p4.add_checkbox_button_widget(show_edges, value=False)


p4.add_background_image('./data/prado.jpg')
p4.show()






