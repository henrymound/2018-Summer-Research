// Generated by gencpp from file dji_sdk/MissionHpGetInfoResponse.msg
// DO NOT EDIT!


#ifndef DJI_SDK_MESSAGE_MISSIONHPGETINFORESPONSE_H
#define DJI_SDK_MESSAGE_MISSIONHPGETINFORESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <dji_sdk/MissionHotpointTask.h>

namespace dji_sdk
{
template <class ContainerAllocator>
struct MissionHpGetInfoResponse_
{
  typedef MissionHpGetInfoResponse_<ContainerAllocator> Type;

  MissionHpGetInfoResponse_()
    : hotpoint_task()
    , cmd_set(0)
    , cmd_id(0)
    , ack_data(0)  {
    }
  MissionHpGetInfoResponse_(const ContainerAllocator& _alloc)
    : hotpoint_task(_alloc)
    , cmd_set(0)
    , cmd_id(0)
    , ack_data(0)  {
  (void)_alloc;
    }



   typedef  ::dji_sdk::MissionHotpointTask_<ContainerAllocator>  _hotpoint_task_type;
  _hotpoint_task_type hotpoint_task;

   typedef uint8_t _cmd_set_type;
  _cmd_set_type cmd_set;

   typedef uint8_t _cmd_id_type;
  _cmd_id_type cmd_id;

   typedef uint32_t _ack_data_type;
  _ack_data_type ack_data;





  typedef boost::shared_ptr< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> const> ConstPtr;

}; // struct MissionHpGetInfoResponse_

typedef ::dji_sdk::MissionHpGetInfoResponse_<std::allocator<void> > MissionHpGetInfoResponse;

typedef boost::shared_ptr< ::dji_sdk::MissionHpGetInfoResponse > MissionHpGetInfoResponsePtr;
typedef boost::shared_ptr< ::dji_sdk::MissionHpGetInfoResponse const> MissionHpGetInfoResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace dji_sdk

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/melodic/share/nav_msgs/cmake/../msg'], 'dji_sdk': ['/home/henry/Documents/SummerResearch2018/Matrice600Pro/src/Onboard-SDK-ROS/dji_sdk/msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/melodic/share/actionlib_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/melodic/share/sensor_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8c08f93488e030961f6001dc630fd2c2";
  }

  static const char* value(const ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8c08f93488e03096ULL;
  static const uint64_t static_value2 = 0x1f6001dc630fd2c2ULL;
};

template<class ContainerAllocator>
struct DataType< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dji_sdk/MissionHpGetInfoResponse";
  }

  static const char* value(const ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "MissionHotpointTask hotpoint_task\n\
\n\
uint8 cmd_set\n\
uint8 cmd_id\n\
uint32 ack_data\n\
\n\
================================================================================\n\
MSG: dji_sdk/MissionHotpointTask\n\
float64 latitude  # degree\n\
float64 longitude # degree\n\
float64 altitude  # meter\n\
float64 radius    # meter\n\
float32 angular_speed #deg/s\n\
uint8 is_clockwise\n\
uint8 start_point\n\
uint8 yaw_mode\n\
";
  }

  static const char* value(const ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.hotpoint_task);
      stream.next(m.cmd_set);
      stream.next(m.cmd_id);
      stream.next(m.ack_data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MissionHpGetInfoResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dji_sdk::MissionHpGetInfoResponse_<ContainerAllocator>& v)
  {
    s << indent << "hotpoint_task: ";
    s << std::endl;
    Printer< ::dji_sdk::MissionHotpointTask_<ContainerAllocator> >::stream(s, indent + "  ", v.hotpoint_task);
    s << indent << "cmd_set: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.cmd_set);
    s << indent << "cmd_id: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.cmd_id);
    s << indent << "ack_data: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.ack_data);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DJI_SDK_MESSAGE_MISSIONHPGETINFORESPONSE_H