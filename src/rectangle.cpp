#include <ros/ros.h>
#include <rviz_visual_tools/rviz_visual_tools.h>

// For visualizing things in rviz
rviz_visual_tools::RvizVisualToolsPtr visual_tools_;

void globalInit(){
    visual_tools_.reset(new rviz_visual_tools::RvizVisualTools("world","/rviz_visual_markers"));
    visual_tools_->loadMarkerPub();
    visual_tools_->deleteAllMarkers();
    visual_tools_->enableBatchPublishing();

    Eigen::Isometry3d pose1 = Eigen::Isometry3d::Identity();
    Eigen::Isometry3d pose2 = Eigen::Isometry3d::Identity();
    pose1.translation().x() = 0.0;
    pose1.translation().y() = 0.0;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 1.23;
    pose2.translation().y() = 0.0;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED, rviz_visual_tools::LARGE);
    visual_tools_->trigger();

    pose1.translation().x() = 1.23;
    pose1.translation().y() = 0.0;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 1.23;
    pose2.translation().y() = 0.69;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED, rviz_visual_tools::LARGE);
    visual_tools_->trigger();

    pose1.translation().x() = 1.23;
    pose1.translation().y() = 0.69;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 0.0;
    pose2.translation().y() = 0.69;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED, rviz_visual_tools::LARGE);
    visual_tools_->trigger();

    pose1.translation().x() = 0.0;
    pose1.translation().y() = 0.69;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 0.0;
    pose2.translation().y() = 0.0;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED, rviz_visual_tools::LARGE);
    visual_tools_->trigger();

}




int main(int argc, char** argv)
{   
    //ROS INTI
    ros::init(argc, argv, "create_rectangle");
    ros::NodeHandle node_handle;
    ros::AsyncSpinner spinner(1);
    spinner.start();

    globalInit();

    //END
    ros::waitForShutdown();
    return 0;
}
