import open3d as o3d
import numpy as np

point_cloud = o3d.io.read_point_cloud("result.ply")

point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)
#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(point_cloud, alpha=0.03)

bbox = point_cloud.get_axis_aligned_bounding_box()
mesh = mesh.crop(bbox)

#o3d.io.write_triangle_mesh("result.obj", mesh)

#viz

o3d.visualization.draw_geometries([point_cloud], window_name="point cloud")
o3d.visualization.draw_geometries([mesh], window_name="mesh")