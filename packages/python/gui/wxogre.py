# Library Includes
import wx
import Ogre

# Projects Include
from sim.simulation import Simulation
from core import cls_property

class wxOgre(wx.PyControl):
    """
    This control creates and Ogre Rendering window relying on the simulation
    to handle the ogre specific part.
    
    @type camera: Ogre.Camera
    @ivar camera: The camera whos view is shown through the viewport
    """    
    def __init__(self, camera, parent, id = -1, pos = wx.DefaultPosition, 
             size = wx.DefaultSize, style = 0, validator = wx.DefaultValidator, 
             name = wx.ControlNameStr):
        wx.PyControl.__init__(self, parent, id, pos, size, style, validator, name)
        
        self._camera = camera
        if camera is not None:
            self._camera.setAutoAspectRatio(True)
        self._init_ogre()
        
        # Setup our event handlers
        self.Bind(wx.EVT_CLOSE, self._on_close)
        #self.Bind(wx.EVT_IDLE, self._update)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._update)
        self.Bind(wx.EVT_SIZE, self._update) 
        
        self._update()
    
    class camera(cls_property):
        """
        The camera attached to the main viewport of the window.
        """
        def fget(self):
            return self._camera
        def fset(self, camera):
            # This ensures the window resizes properly
            camera.setAutoAspectRatio(True)
            
            if self._camera is None:
                self._viewport = self._render_window.addViewport(camera)
            else:
                self._viewport.setCamera(camera)
            self._camera = camera
            # Refresh the window
            self._update()
    
    def _init_ogre(self):
        """
        Hook ogre up to the control.  On Linux this must be called after your
        top level frame has recived its first activate event, or after its
        contructor has finished. I suggest you do so for all platforms for 
        simplicity.
        """
        self._create_ogre_window()
        self._render_window.update()
            
    def _update(self, event = None):
        """
        Handles all events that require redrawing
        """
        # Resize the window on resize
        if type(event) is wx.SizeEvent:
            # On GTK we let Ogre create its own child window, so we have to
            # manually resize it match its parent, this control
            if '__WXGTK__' == wx.Platform:
                size = self.GetClientSize()
                self._render_window.resize(size.width, size.height)
            self._render_window.windowMovedOrResized()
        
        # Redraw the window for every event
        self._render_window.update()
        #Ogre.Root.getSingleton().renderOneFrame()
        if event is not None:
            event.Skip()
            
    def _on_close(self, event):
        self._render_window.removeAllViewports()
        self._render_window.destroy()
    
    def _create_ogre_window(self):
        size = self.GetClientSize()
        params = self._get_window_params()
        
        self._render_window = \
            Simulation.get().create_window(self.GetName(), size.width, 
                                           size.height, params)
            
        self._render_window.active = True
        # You can only create a camera after you have made the first render
        # window, so check to see if we are given a camera
        if self._camera is not None:
            self._viewport = self._render_window.addViewport(self._camera)
            
    def _get_window_params(self):
        """
        Encapsulates the platform specific part of the window creation, grabing
        the windows handle and transforming them for Ogre.
        """
        params = Ogre.NameValuePairList()
        
        if '__WXGTK__' == wx.Platform:
            raise Exception('Support for Linux not yet integrated')
        elif '__WXMSW__' == wx.Platform:
            params['externalWindowHandle'] = str(self.GetHandle())
        else:
            raise Exception('%s no yet supported' % wx.Platform)
        
        return params