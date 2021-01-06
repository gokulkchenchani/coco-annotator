# @Author: Claus Smitt
# @Date:   2020-12-07 17:03:38
# @Last Modified by:   Claus Smitt
# @Last Modified time: 2020-12-07 17:04:24

# Get installer script absolute path
INSTALLER_PATH="`dirname \"$0\"`"              # relative
INSTALLER_PATH="`( cd \"$INSTALLER_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$INSTALLER_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  echo "Error: Unable to find installers path. Possible permissions issue"
  exit 1  # fail
fi

echo "AgRobot anotator PyTorch and CUDA support installer"

# Generate deploy keys for cloning repos
$INSTALLER_PATH/repos-keygen.sh $INSTALLER_PATH
# Install nvidia interface for docker
$INSTALLER_PATH/nvidia-container-runtime-installer.sh $INSTALLER_PATH
# Build torch environment container
$INSTALLER_PATH/build-torch-env.sh $INSTALLER_PATH
