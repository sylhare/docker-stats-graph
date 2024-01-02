from src.dockerstats import *

ds = DockerStats("data.csv")

ds.plot_category_live('MEM Usage')
