// Generated by gencpp from file dji_sdk/QueryDroneVersionResponse.msg
// DO NOT EDIT!


#ifndef DJI_SDK_MESSAGE_QUERYDRONEVERSIONRESPONSE_H
#define DJI_SDK_MESSAGE_QUERYDRONEVERSIONRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace dji_sdk
{
template <class ContainerAllocator>
struct QueryDroneVersionResponse_
{
  typedef QueryDroneVersionResponse_<ContainerAllocator> Type;

  QueryDroneVersionResponse_()
    : version(0)
    , hardware()  {
    }
  QueryDroneVersionResponse_(const ContainerAllocator& _alloc)
    : version(0)
    , hardware(_alloc)  {
  (void)_alloc;
    }



   typedef uint32_t _version_type;
  _version_type version;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _hardware_type;
  _hardware_type hardware;





  typedef boost::shared_ptr< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> const> ConstPtr;

}; // struct QueryDroneVersionResponse_

typedef ::dji_sdk::QueryDroneVersionResponse_<std::allocator<void> > QueryDroneVersionResponse;

typedef boost::shared_ptr< ::dji_sdk::QueryDroneVersionResponse > QueryDroneVersionResponsePtr;
typedef boost::shared_ptr< ::dji_sdk::QueryDroneVersionResponse const> QueryDroneVersionResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace dji_sdk

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/melodic/share/nav_msgs/cmake/../msg'], 'dji_sdk': ['/home/henry/Documents/SummerResearch2018/Matrice600Pro/src/Onboard-SDK-ROS/dji_sdk/msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/melodic/share/actionlib_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/melodic/share/sensor_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/melodic/share/geometry_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "89b6e8d274e31334cc3a372757607be2";
  }

  static const char* value(const ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x89b6e8d274e31334ULL;
  static const uint64_t static_value2 = 0xcc3a372757607be2ULL;
};

template<class ContainerAllocator>
struct DataType< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dji_sdk/QueryDroneVersionResponse";
  }

  static const char* value(const ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint32 version\n\
string hardware\n\
";
  }

  static const char* value(const ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.version);
      stream.next(m.hardware);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct QueryDroneVersionResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dji_sdk::QueryDroneVersionResponse_<ContainerAllocator>& v)
  {
    s << indent << "version: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.version);
    s << indent << "hardware: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.hardware);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DJI_SDK_MESSAGE_QUERYDRONEVERSIONRESPONSE_H
