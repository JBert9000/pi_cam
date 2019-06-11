from pi_cam import df

from bokeh.plotting import figure, show, output_file

p=figure(x_axis_type='datetime',height=300,width=1500,title="Motion Graph")

q=p.quad(left=df["Start"],right=df["End"],bottom=0,top=1,color="green")

output_file("Graph.html")
show(p)
