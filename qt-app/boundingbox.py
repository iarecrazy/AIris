# import sys
# from enum import Enum


		

# class BoundingBox:
# 	class Mode(Enum):
# 		NONE 	 = 0
# 		RESIZING = 1
# 		DRAGGING = 2

# 	def __init__(self, view):
# 		# set up pens and brushes
# 		self.normalPen 			= QPen	(QColor(255,0,0,128), 5)
# 		self.normalBrush		= QBrush(QColor(255,0,0,50))
# 		self.hoverPen 			= QPen	(QColor(255,0,0,228), 10)
# 		self.hoverBrush			= QBrush(QColor(255,0,0,100))

# 		# store the QGraphicsRectItem
# 		self.view				= view
# 		self.myRect 			= self.view.scene().addRect(QRectF(self.startingPoint.x(), self.startingPoint.y(), 5, 5), self.normalPen, self.normalBrush)
# 		self.mode 				= Mode.RESIZING

# 	def eventToScenePoint(self, event, view):
# 		return view.mapToScene(QPoint(event.x(), event.y()))

# 	def thatsMe(self, rect):
# 		return rect == self.myRect

# 	def mousePressEvent(self, event, view):
# 		# map the current mouse position to scene coordinates using the view
# 		point = self.eventToScenePoint(event, view)

# 		# this event hits me
# 		bool imHit = self.myRect.contains(point)

# 		if(self.mode == Mode.RESIZING):


