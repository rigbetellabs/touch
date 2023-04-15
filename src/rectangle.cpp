#include <ros/ros.h>
#include <rviz_visual_tools/rviz_visual_tools.h>

// For visualizing things in rviz
rviz_visual_tools::RvizVisualToolsPtr visual_tools_;
float pose_x, pose_y;

void globalInit(){
    visual_tools_.reset(new rviz_visual_tools::RvizVisualTools("world","/rviz_visual_markers"));
    visual_tools_->loadMarkerPub();
    visual_tools_->deleteAllMarkers();
    visual_tools_->enableBatchPublishing();

}

void createRectangle (){
    visual_tools_->deleteAllMarkers();
    visual_tools_->trigger();
    Eigen::Isometry3d pose1 = Eigen::Isometry3d::Identity();
    Eigen::Isometry3d pose2 = Eigen::Isometry3d::Identity();
    pose1.translation().x() = 0.0;
    pose1.translation().y() = 0.0;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = pose_x;
    pose2.translation().y() = 0.0;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED, rviz_visual_tools::MEDIUM);
    visual_tools_->trigger();

    pose1.translation().x() = pose_x;
    pose1.translation().y() = 0.0;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = pose_x;
    pose2.translation().y() = pose_y;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED);
    visual_tools_->trigger();

    pose1.translation().x() = pose_x;
    pose1.translation().y() = pose_y;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 0.0;
    pose2.translation().y() = pose_y;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED);
    visual_tools_->trigger();

    pose1.translation().x() = 0.0;
    pose1.translation().y() = pose_y;
    pose1.translation().z() = 0.0;
    
    pose2.translation().x() = 0.0;
    pose2.translation().y() = 0.0;
    pose2.translation().z() = 0.0;
    visual_tools_->publishLine(pose1.translation(), pose2.translation(),rviz_visual_tools::RED);

    visual_tools_->trigger();
    ROS_DEBUG_STREAM("Created Rectangle : "<< pose_x << " "<< pose_y <<" ");
}


int main(int argc, char** argv)
{   
    //ROS INTI
    ros::init(argc, argv, "create_rectangle");
    ros::NodeHandle node_handle("create_rectangle");
    ros::AsyncSpinner spinner(1);
    spinner.start();

    globalInit();
    while (ros::ok()){
        if(!node_handle.getParam("pose_x", pose_x))
            ROS_INFO_STREAM("Failed to get X : "<< pose_x );
        
        if(!node_handle.getParam("pose_y", pose_y))
            ROS_INFO_STREAM("Failed to get Y : "<< pose_y );
        
        createRectangle();
        ros::Duration(0.5).sleep();
    }
    //END
    ros::waitForShutdown();
    return 0;
}
