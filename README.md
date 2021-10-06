# CapstoneProject
# Dynamic Radial Tree layout Visualization

![image](https://user-images.githubusercontent.com/70006591/117807515-4c4ac200-b28e-11eb-8544-ab69e1e926b2.png)

# Project overview

Project Title: Intelligent Bibliometrics for Knowledge Discovery

overview:<br>
Bibliometrics is known as the development and application of statistical approaches for analysing scientific documents (e.g., research articles, patents, and academic proposals), and its incorporation with artificial intelligence techniques, we call intelligent bibliometrics, further enhances its capabilities in handling large scale data analytics, discovering latent and complicated relationships, and developing robust models.

University of Technology Sydney

Supervisors: Yi Zhang, Mengjia Wu

Team members: <br>
Hang Sheng 13665664 <br>
Longhao Zhu 13674938<br>
Xiaoju Ma 13261185<br>
Zhenhuan Yu 13491865<br>
Anthony Ghassibe 13207550<br>


## Key library Version <br>
networkx:  2.5.1 <br>
community :  0.15 <br>

## Install the key library
pip install networkx <br>
pip install python-louvain <br>

if you have installed community, please use "pip uninstall community" to uninstall the community library and then install the python-Louvain library.

## The meaning of each directory

![image](https://user-images.githubusercontent.com/70006591/117805165-3b4c8180-b28b-11eb-9c32-244b8f49a3e8.png)

1.dataset: store two kinds of datasets, the pair of “node.csv” and “edge.csv” is what mengjia provided us at the beginning of this semester. The pair of “Nodes.csv” and “Edges.csv” is the set that mengjia provided us to test whether our visualization system is adaptive.

2.Processed data: store the json file after running the “csv_to_json.py” python script, this json file will be imported in the visualization layout.

3.visualization layout: Vega codes for the visualization layout.

## Operation guidance

1.Select the dataset you want to converted, the community detection choice you want and run the script “csv_to_json.py” file. 

![image](https://user-images.githubusercontent.com/70006591/118007284-98752f80-b37e-11eb-9dff-b9df093aad84.png)

If you select “choice = 2” in community_detection(), you will type the number of resolution and whether you want to consider weight.

Resolution: By default 1.0, the higher the value, the fewer the number of communities.

![image](https://user-images.githubusercontent.com/70006591/118007921-2fda8280-b37f-11eb-9fbb-7fe6c9d1ad9c.png)

2.Select the visualization layout in the file “run_vega_visualization”

![image](https://user-images.githubusercontent.com/70006591/118007423-b5116780-b37e-11eb-9056-11d509108534.png)

spec1: General Tree layout<br>
spec2: Radial Tree layout <br>

Then run the html file in browser (Recommend Google Chrome) in either one way below:

![image](https://user-images.githubusercontent.com/70006591/118007527-cc505500-b37e-11eb-9cdf-2ccb999fa249.png)

3.Scroll the bars on the right and below until you see the initial node

![image](https://user-images.githubusercontent.com/70006591/118008173-6c0de300-b37f-11eb-95aa-63f27663ecbc.png)

Scroll to the bottom left corner of the page until you can see a series of navigation boxes.

![image](https://user-images.githubusercontent.com/70006591/118008287-7fb94980-b37f-11eb-879a-584f3ad7d957.png)

Move the node in the “year” bar and then you will see the change in the graph.

## Description for other navigation bars
1.label: display the node label or not in the graph. <br>
2.nodeSize: change the node size based on the “record” attribute 	in the node dataset. (Avoid the node overlap)  <br>
3.edgeSize: change the edge size based on the “weight” attribute 	in the edge dataset.  <br>
4.textSize: change the size of label name for each node. (Avoid the text overlap)  <br>
5.radius: change the radius of the radial tree (Avoid the node overlap and text overlap)  <br>
6.rotate: rotate the radial tree graph (Avoid the text overlap)   <br>
7.links: shape type of the link  <br>

## Graphical attributes meanings
1.Current year will be display in the middle of the graph

![image](https://user-images.githubusercontent.com/70006591/117805258-55865f80-b28b-11eb-9e78-b6b3acdf5b56.png)


2.If user hovers the mouse in the node, he/she will see the node information (with the border color changing to green): name + time interval

![image](https://user-images.githubusercontent.com/70006591/117805268-57e8b980-b28b-11eb-97b7-6c454720c862.png)

3.If user hovers the mouse in the edge, he/she will see the edge information (with the edge color changing to yellow): source -> target, edge weight, time interval.

![image](https://user-images.githubusercontent.com/70006591/117805275-5a4b1380-b28b-11eb-9e7d-9c2696c27c64.png)

4.As year goes by, some nodes will be invalid (current year > node’s end year), all these invalid node will be converted to hollow circle with orange border, with the disappearance of the label name. But the user still can know the information of this node if hovering the mouse in it.

![image](https://user-images.githubusercontent.com/70006591/117805285-5cad6d80-b28b-11eb-8298-b765c2412b16.png)

5.As year goes by, some edges will be invalid as well (current year > weight’s end year), all these invalid line will be converted into orange dashed line. The user can still know the information of this edge if hovering the mouse in it.

![image](https://user-images.githubusercontent.com/70006591/117805294-5f0fc780-b28b-11eb-9a3a-2a80ab53eccd.png)

6.The different colors of the nodes represent that the nodes are located in different communities, the nodes in the same community mean they have a certain relationship.

For example, the screenshot below shows four different communities with some nodes in each of them. The dead node displayed as a hollow circle with an orange border is not located in any community any more, if the user wants to know which community the dead nodes locate, they can move back to the previous years to see it.

![image](https://user-images.githubusercontent.com/70006591/119003034-fb3e7a80-b9bf-11eb-86ac-db7d6d3243eb.png)


If the end year of all edges and edges are reached, all nodes and edges will become invalid, the graph will become like this:

![image](https://user-images.githubusercontent.com/70006591/118010223-687b5b80-b381-11eb-915c-0a45bbb7823c.png)

7. Additional functions

In addition, when the user moves to the upper right corner of the page, he can see a button with three dots. When the user clicks this button, the following four options will appear, their meanings are:

Save as SVG: The current graph will be downloaded as a SVG image. SVG is a vector image format which uses geometric forms to represent different parts as discrete objects and are infinitely scalable. <br>

Save as PNG: The current graph will be downloaded as a PNG image. <br>

View Source: The layout visualization source code will be viewed. <br>

Open in Vega Editor: The online Vega editor will be opened but the graph will not display, the user should manually change the dataset input path in the online editor. <br>

![image](https://user-images.githubusercontent.com/70006591/119003205-20cb8400-b9c0-11eb-937e-a2c2bb59ae73.png)


## Alternative tree layout visualization

There is an alternative tree layout visualization provided, the user can simply change the variable here.

![image](https://user-images.githubusercontent.com/70006591/118007034-5ba93880-b37e-11eb-875e-96d643fb6246.png)

![image](https://user-images.githubusercontent.com/70006591/118008724-ee96a280-b37f-11eb-98ca-1183f0beae2b.png)

The purpose of this alternative tree layout visualization is to avoid the label overlap and give intuition to users about the hierarchical level of the tree.

## One more important thing
If you change other dataset, you should change the signal range in both “General_Tree.json” and “Radial_Tree.json” files.

![image](https://user-images.githubusercontent.com/70006591/118012080-45ea4200-b383-11eb-967a-ea3400540666.png)

The min and max value can be referenced in the start year and the end year of the root node in the “Radial_Tree_data.json” after you run the “csv_to_json.py” script.

![image](https://user-images.githubusercontent.com/70006591/118012126-513d6d80-b383-11eb-8b22-864c966bed33.png)
