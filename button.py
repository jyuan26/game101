"""
Button.py 
Benjamin Bouie 
"""
from graphics import * 

# class button 
class Button: 
    """ constructs a rectangular Button object
        centered at the Point center with given
        width, height, and label (text on button).
        The button should be inactive when
        constructed
    """
    def __init__(self,center,width, height, label): 
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
        "makes clicks on button have no effect on the program"
        self.active = False
        self.label.setStyle("italic")
        self.outline.setFill("grey89")
        self.outline.setWidth(1)

    def activate(self):
        "makes button clickable"
        self.active = True 
        self.outline.setFill("cyan4")
        self.label.setStyle("normal")
        self.outline.setWidth(2)

    def draw(self, win):
        """draws the button on the
        graphics window win"""

        self.outline.draw(win)
        self.label.draw(win)

    def undraw(self):
        """undraws the button from the
        graphics window"""
        self.deactivate()
        self.outline.undraw()
        self.label.undraw()

    def getLabel(self): 
        "returns current button label"
        return self.label.getText() 

    def setLabel(self, newText):  
        "changes label on button to newText"
        self.label.setText(newText)
        # This can't be just `self.label = newText` because that would be 
        # bad practice (we want encapsulation)

    def clicked(self, pt): 
        """returns bool True if the button is active and Point pt is on the
        button; otherwise it returns False"""
        xPt = pt.getX()
        yPt = pt.getY()
        if self.xmin < xPt < self.xmax: 
            if self.ymin < yPt < self.ymax: 
                return True 
        else: 
            return False

def main(): 
    win = GraphWin()
    test = Button(Point(100,100), 75, 50, "start") 
    test.activate()
    test.draw(win)

    win.getMouse()

if __name__ == "__main__": main()


