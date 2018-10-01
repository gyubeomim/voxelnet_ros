import numpy as np

import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

def hv_in_range(x, y, z, fov, fov_type='h'):
	"""
	Extract filtered in-range velodyne coordinates based on azimuth & elevation angle limit

	Args:
	`x`:velodyne points x array
	`y`:velodyne points y array
	`z`:velodyne points z array
	`fov`:a two element list, e.g.[-45,45]
	`fov_type`:the fov type, could be `h` or 'v',defualt in `h`

	Return:
	`cond`:condition of points within fov or not

	Raise:
	`NameError`:"fov type must be set between 'h' and 'v' "
	"""
	d = np.sqrt(x ** 2 + y ** 2 + z ** 2)
	if fov_type == 'h':
		return np.logical_and(np.arctan2(y, x) > (-fov[1] * np.pi/180), np.arctan2(y, x) < (-fov[0] * np.pi/180))
	elif fov_type == 'v':
		return np.logical_and(np.arctan2(z, d) < (fov[1] * np.pi / 180), np.arctan2(z, d) > (fov[0] * np.pi / 180))
	else:
		raise NameError("fov type must be set between 'h' and 'v' ")


def velo_cb(msg):
    global pcl_msg, cond, np_p, np_p_ranged
    pcl_msg = pc2.read_points(msg, skip_nans=False)
    np_p = np.array(list(pcl_msg), dtype=np.float32)
    np_p = np.delete(np_p, -1, 1)

    cond = hv_in_range(x=np_p[:,0],
    y=np_p[:,1],
    z=np_p[:,2],
    fov=[-45,45],
    fov_type='h')

    np_p_ranged = np_p[cond]

rospy.init_node('test_node')

sub = rospy.Subscriber('/velodyne_points', PointCloud2, velo_cb)
