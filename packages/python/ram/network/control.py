
import ext.core as core
import ext.math as math
import ext.control as control
import ext.estimation as estimation
import ext.network as network
import ext.vehicle as vehicle

class RemoteController(core.Subsystem):
    def __init__(self, config, deps):
        core.Subsystem.__init__(self, config.get('name', 'RemoteController'))

        self._eventHub = core.Subsystem.getSubsystemOfType(
            core.QueuedEventHub, deps, nonNone = True)
        self._controller = core.Subsystem.getSubsystemOfType(
            control.IController, deps, nonNone = True)
        self._estimator = core.Subsystem.getSubsystemOfType(
            estimation.IStateEstimator, deps, nonNone = True)
        self._vehicle = core.Subsystem.getSubsystemOfType(
            vehicle.IVehicle, deps)

        self._yawChange = config.get('yawChange', 10)
        self._speed, self._tspeed = 0, 0

        self._connections = []

        registrationInfo = ['EMERGENCY_STOP', 'YAW_LEFT', 'YAW_RIGHT',
                            'PITCH_UP', 'PITCH_DOWN', 'ROLL_LEFT',
                            'ROLL_RIGHT', 'FORWARD_MOVEMENT',
                            'DOWNWARD_MOVEMENT', 'LEFT_MOVEMENT',
                            'RIGHT_MOVEMENT', 'DESCEND', 'ASCEND',
                            'SETSPEED', 'TSETSPEED', 'ANGLEYAW',
                            'ANGLEPITCH', 'ANGLEROLL',
                            'FIRE_MARKER_DROPPER', 'FIRE_TORPEDO_LAUNCHER']
                            
        for type_ in registrationInfo:
            realType = getattr(network.EventType, type_)
            handler = getattr(self, '_%s' % type_.lower())
            self._registerForEvent(realType, handler)

    def __del__(self):
        for conn in self._connections:
            conn.disconnect()

    def _registerForEvent(self, type_, callback):
        conn = self._eventHub.subscribeToType(type_, callback)
        self._connections.append(conn)

    def _emergency_stop(self, event):
        # Safe the thrusters (if vehicle is available)
        if self._vehicle is not None:
            self._vehicle.safeThrusters()

    def _yaw_left(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, 0, rate))

    def _yaw_right(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, 0, rate))

    def _pitch_up(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, rate, 0))

    def _pitch_down(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, rate, 0))

    def _roll_left(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(rate, 0, 0))

    def _roll_right(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(rate, 0, 0))

    def _forward_movement(self, event):
        pass

    def _downward_movement(self, event):
        pass

    def _left_movement(self, event):
        pass

    def _right_movement(self, event):
        pass

    def _descend(self, event):
        depth = self._estimator.getEstimatedDepth()
        self._controller.changeDepth(depth, 3)

    def _ascend(self, event):
        depth = self._estimator.getEstimatedDepth()
        self._controller.changeDepth(depth, -3)

    def _setspeed(self, event):
        self._speed = event.number
        self._setvelocity()

    def _tsetspeed(self, event):
        self._tspeed = event.number
        self._setvelocity()

    def _setvelocity(self):
        """
        This is a documentation comment.
        """
        pos = self._estimator.getEstimatedPosition()
        yaw = self._estimator.getEstimatedOrientation().getYaw().valueRadians()
        nRb = math.nRb(yaw)
        #self._controller.translate(
        #    pos, nRb * math.Vector2(self._speed, self._tspeed))

    def _angleyaw(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, 0, rate))

    def _anglepitch(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(0, rate, 0))

    def _angleroll(self, event):
        ori = self._estimator.getEstimatedOrientation()
        rate = event.number
        self._controller.rotate(ori, math.Vector3(rate, 0, 0))

    def _fire_marker_dropper(self, event):
        self._vehicle.dropMarker()

    def _fire_torpedo_launcher(self, event):
        self._vehicle.fireTorpedo()

core.SubsystemMaker.registerSubsystem('RemoteController', RemoteController)