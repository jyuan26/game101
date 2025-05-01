"""
Button.py 
Benjamin Bouie 
"""
from graphics import * 

class Button: 
    """ 
    A clickable rectangular button with a text label.
    
    The Button class provides methods to create, draw, activate/deactivate,
    and detect clicks on UI buttons. Buttons can be in an active (clickable)
    or inactive (disabled) state with different visual appearances.
    """
    def __init__(self,center,width, height, label): 
        """
        Initialize a new Button object.
        
        Args:
            center: Point object representing the center of the button
            width: Width of the button in pixels
            height: Height of the button in pixels
            label: Text to display on the button
        """
        self.xmin = center.getX() - width / 2
        self.xmax = center.getX() + width / 2 
        self.ymin = center.getY() - height / 2
        self.ymax = center.getY() + height / 2

        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)

        self.outline = Rectangle(p1,p2) 
        self.label = Text(center, label)

        self.deactivate()

    def deactivate(self):
        """
        Deactivate the button (make it unclickable).
        
        Changes the button's appearance to indicate it is inactive:
        - Text becomes italic
        - Background color becomes light grey
        - Border becomes thinner
        """
        self.active = False
        self.label.setStyle("italic")
        self.outline.setFill("grey89")
        self.outline.setWidth(1)

    def activate(self):
        """
        Activate the button (make it clickable).
        
        Changes the button's appearance to indicate it is active:
        - Text becomes normal style
        - Background color becomes cyan
        - Border becomes thicker
        """
        self.active = True 
        self.outline.setFill("cyan4")
        self.label.setStyle("normal")
        self.outline.setWidth(2)

    def draw(self, win):
        """
        Draw the button on the graphics window.
        
        Args:
            win: GraphWin object where the button should be drawn
        """
        self.outline.draw(win)
        self.label.draw(win)

    def undraw(self):
        """
        Remove the button from the graphics window.
        
        Also deactivates the button to ensure proper state if redrawn.
        """
        self.deactivate()
        self.outline.undraw()
        self.label.undraw()

    def getLabel(self): 
        """
        Get the current button label text.
        
        Returns:
            String containing the button's label
        """
        return self.label.getText() 

    def setLabel(self, newText):  
        """
        Change the button's label text.
        
        Args:
            newText: New text to display on the button
        """
        self.label.setText(newText)
        # This can't be just `self.label = newText` because that would be 
        # bad practice (we want encapsulation)

    def clicked(self, pt): 
        """
        Check if a point is inside the button.
        
        Args:
            pt: Point object representing a click location
            
        Returns:
            Boolean indicating whether the point is inside the button
        """
        xPt = pt.getX()
        yPt = pt.getY()
        if self.xmin < xPt < self.xmax: 
            if self.ymin < yPt < self.ymax: 
                return True 
        return False

def main(): 
    """
    Run a simple test of the Button class.
    
    Creates a window with a button and waits for a mouse click.
    """
    win = GraphWin()
    test = Button(Point(100,100), 75, 50, "start") 
    test.activate()
    test.draw(win)

    win.getMouse()

if __name__ == "__main__": main()


