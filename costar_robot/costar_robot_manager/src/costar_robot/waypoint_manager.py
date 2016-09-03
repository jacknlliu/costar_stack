import rospy
import yaml
import tf
import tf_conversions.posemath as pm

from predicator_msgs.srv import *
from predicator_msgs.msg import *

from librarian_msgs.srv import *
from librarian_msgs.msg import *

'''
Set up a basic waypoint manager. This object will store a list of joint space
or cartesian waypoints (the later relative to some frame of reference).

These are stored in Librarian and get loaded any time the system comes up.
'''
class WaypointManager:

  def __init__(self,world="world",ns="",endpoint="/endpoint",):
    self.tf_publisher = tf.TransformBroadcaster()
    rospy.wait_for_service('/librarian/add_type',5)
    self.add_type_service = rospy.ServiceProxy('/librarian/add_type', librarian_msgs.srv.AddType)
    self.save_service = rospy.ServiceProxy('/librarian/save', librarian_msgs.srv.Save)
    self.load_service = rospy.ServiceProxy('/librarian/load', librarian_msgs.srv.Load)
    self.list_service = rospy.ServiceProxy('/librarian/list', librarian_msgs.srv.List)
    self.delete_service = rospy.ServiceProxy('/librarian/delete', librarian_msgs.srv.Delete)

    self.world = world
    self.endpoint = endpoint

    self.js_waypoints = {}
    self.js_waypoint_names = {}
    self.cart_waypoints = {}
    self.cart_waypoint_names = {}
    self.all_js_moves = []

    self.update()

  '''
  Update list of frames from librarian
  '''
  def update(self):
    
    # ----------------------------------------
    # this section loads joint space waypoints
    js_filenames = self.list_service(self.js_folder).entries

    for name in js_filenames:
      data = yaml.load(self.load_service(id=name,type=self.js_folder).text)
      if not data[1] in self.waypoints.keys():
        self.js_waypoints[data[1]] = []
        self.js_waypoint_names[data[1]] = []

        self.js_waypoints[data[1]].append(data[0])
        self.js_waypoint_names[data[1]].append(name)
        self.all_js_moves.append(data[1] + "/" + name)

    print " === LOADING === "
    print self.waypoint_names
    print self.waypoints
    print self.js_waypoint_names
    print self.js_waypoint

    # ----------------------------------------
    # this section loads cartesian waypoints

    cart_filenames = self.list_service(self.cart_folder).entries
    for name in cart_filenames:
      data = yaml.load(self.load_service(id=name,type=self.cart_folder).text)

  '''
  Save frame to library if necessary
  '''
  def save_frame(self, frame, reference, name):
    pass

  '''
  Save joints to library if necessary
  '''
  def save_joints(self, joints, name):
      self.save_service(id=name.strip('/'),type=self.js_folder,text=yaml.dump(joints))

  '''
  Find a saved frame and return it
  '''
  def lookup_frame(self, name, reference):
    pass

  '''
  Display TF positions of all possible waypoints.
  '''
  def publish_tf(self):
    pass

  '''
  implement service to get joint states
  '''
  def get_joint_states_by_name_srv(self, req):
      if req.name in self.js_waypoints
          msg = LookupJointStatesResponse(joint_states=self.js_waypoints[name], ack='SUCCESS')
      else:
          msg = LookupJointStatesResponse(ack='FAILURE - %s not found'%req.name)
      return msg
