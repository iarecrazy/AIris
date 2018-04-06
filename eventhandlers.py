from enum import Enum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# event handler base class for mouse based event handlers
class ViewEventHandler:
	class EventState:
		def __init__(self):
			self.leftButtonDown		= False
			self.middleButtonDown	= False
			self.rightButtonDown	= False
			self.eventPoint 		= QPoint(0,0)
			self.scenePoint			= QPointF(0,0)

		def copy(self):
			state = ViewEventHandler.EventState()
			
			state.leftButtonDown 	= self.leftButtonDown
			state.middleButtonDown 	= self.middleButtonDown
			state.rightButtonDown 	= self.rightButtonDown
			state.eventPoint 		= self.eventPoint
			state.scenePoint 		= self.scenePoint

			return state

	def __init__(self, view):
		self.view = view
		self.prevState = ViewEventHandler.EventState()

	# --- helper methods ---

	def eventToScenePoint(self, event):
		return self.view.mapToScene(QPoint(event.x(), event.y()))
	
	def buttonDownCount(self, currentState):
		i = 0
		if(currentState.leftButtonDown):
			i = i + 1
		if(currentState.rightButtonDown):
			i = i + 1
		if(currentState.middleButtonDown):
			i = i + 1
		return i

	def noButtonsPressed(self, currentState):
		return self.buttonDownCount(currentState) == 0	

	def multipleButtonsPressed(self, currentState):
		return self.buttonDownCount(currentState) > 1

	def wasLeftButtonReleased(self, currentState, previousState):
		return currentState.leftButtonDown == False and previousState.leftButtonDown == True

	def wasMiddleButtonReleased(self, currentState, previousState):
		return currentState.middleButtonDown == False and previousState.middleButtonDown == True

	def wasRightButtonReleased(self, currentState, previousState):
		return currentState.rightButtonDown == False and previousState.rightButtonDown == True

	def wasLeftButtonPressed(self, currentState, previousState):
		return currentState.leftButtonDown == True and previousState.leftButtonDown == False

	def wasMiddleButtonPressed(self, currentState, previousState):
		return currentState.middleButtonDown == True and previousState.middleButtonDown == False

	def wasRightButtonPressed(self, currentState, previousState):
		return currentState.rightButtonDown == True and previousState.rightButtonDown == False

	# internal event handler - do not directly override these
	def mousePressEvent(self, event):
		# copy the state & update the point
		newState			= self.prevState.copy()
		newState.eventPoint = QPoint(event.x(), event.y())
		newState.scenePoint = self.eventToScenePoint(event)

		button = event.button()

		if 	(button == Qt.LeftButton):
			newState.leftButtonDown = True
		elif(button == Qt.RightButton):
			newState.rightButtonDown = True
		elif(button == Qt.MiddleButton):
			newState.middleButtonDown = True

		self.mousePressEvent_(newState, self.prevState)

		# update state
		self.prevState = newState

	def mouseMoveEvent(self, event):
		# copy the state & update the point
		newState		= self.prevState.copy()
		newState.eventPoint = QPoint(event.x(), event.y())
		newState.scenePoint = self.eventToScenePoint(event)

		# on a mousemove event event.button() is always NoButton, no need to update buttons
		self.mouseMoveEvent_(newState, self.prevState)

		# update state
		self.prevState = newState

	def mouseReleaseEvent(self, event):
		# copy the state & update the point
		newState		= self.prevState.copy()
		newState.eventPoint = QPoint(event.x(), event.y())
		newState.scenePoint = self.eventToScenePoint(event)

		button = event.button()

		if 	(button == Qt.LeftButton):
			newState.leftButtonDown = False
		elif(button == Qt.RightButton):
			newState.rightButtonDown = False
		elif(button == Qt.MiddleButton):
			newState.middleButtonDown = False

		# on a mousemove event event.button() is always NoButton, no need to update buttons
		self.mouseReleaseEvent_(newState, self.prevState)

		# update state
		self.prevState = newState

	# --- override these for creating your own eventhandler ---
	def mousePressEvent_(self, currentState, previousState):
		pass

	def mouseMoveEvent_ (self, currentState, previousState):
		pass

	def mouseReleaseEvent_(self, currentState, previousState):
		pass

class BoundingBoxEventHandler(ViewEventHandler):
	class Mode(Enum):
		NONE 	= 1
		CREATE 	= 2
		DRAG 	= 3
		HOVER 	= 4

	def __init__(self, view):
		super().__init__(view)
		self.mode 			= BoundingBoxEventHandler.Mode.NONE
		self.boundingRect 	= None

		# define the default pens and brushes
		self.normalPen			= QPen	(QColor(255,0,0,128), 5)
		self.normalBrush		= QBrush(QColor(255,0,0,50))
		self.hoverPen 			= QPen	(QColor(255,0,0,228), 10)
		self.hoverBrush			= QBrush(QColor(255,0,0,100))

		self.actionStartPoint 	= QPointF(0,0)
		self.currentRect 		= None

	def setBoundingRect(self, boundingRect):
		self.boundingRect = boundingRect

	def mousePressEvent_(self, currentState, previousState):
		super().mousePressEvent_(currentState, previousState)

		# only do something if one button is pressed
		if(self.multipleButtonsPressed(currentState) == False):

			# if the left button was pressed, we create a new bounding box
			if(self.wasLeftButtonPressed(currentState, previousState)):
				# add code for creating a boundingbox
				self.Mode = BoundingBoxEventHandler.Mode.CREATE
				
				self.currentRect = self.view.scene().addRect(QRectF(currentState.scenePoint.x(), currentState.scenePoint.y(), 5, 5), self.normalPen, self.normalBrush)
				self.currentRect.setAcceptHoverEvents(True)
				self.actionStartPoint = currentState.scenePoint

			# if middle button was pressed and we're hovering over a bounding box, enable drag mode
			elif(self.wasMiddleButtonPressed(currentState, previousState)):
				if(self.Mode == BoundingBoxEventHandler.Mode.HOVER):
					self.Mode = BoundingBoxEventHandler.Mode.DRAG
			
			# if the right button was pressed do nothing for now
			elif(self.wasRightButtonPressed(currentState, previousState)):
				pass

	def mouseMoveEvent_(self, currentState, previousState):
		super().mouseMoveEvent_(currentState, previousState)
		
		if(self.Mode == BoundingBoxEventHandler.Mode.NONE):

			item = self.view.itemAt(currentState.eventPoint)

			if(type(item) == QGraphicsRectItem):
				self.Mode = BoundingBoxEventHandler.Mode.HOVER
				item.setPen(self.hoverPen)
				item.setBrush(self.hoverBrush)
				self.currentRect = item

		elif(self.Mode == BoundingBoxEventHandler.Mode.HOVER):
			
			if(self.currentRect.contains(currentState.scenePoint) == False):
				self.Mode = BoundingBoxEventHandler.Mode.NONE

				self.currentRect.setPen(self.normalPen)
				self.currentRect.setBrush(self.normalBrush)

				self.currentRect = None

		elif(self.Mode == BoundingBoxEventHandler.Mode.CREATE):
			# make sure we're still in the image
			if(self.boundingRect.contains(currentState.scenePoint)):
				x = min(currentState.scenePoint.x(), self.actionStartPoint.x())
				y = min(currentState.scenePoint.y(), self.actionStartPoint.y())

				rect = self.currentRect.setRect(x, y, abs(currentState.scenePoint.x() - self.actionStartPoint.x()), abs(currentState.scenePoint.y() - self.actionStartPoint.y()))
		elif(self.Mode == BoundingBoxEventHandler.Mode.DRAG):
			rect = self.currentRect.rect()
			rect.translate(currentState.scenePoint.x() - previousState.scenePoint.x(), currentState.scenePoint.y() - previousState.scenePoint.y())
			
			if(self.boundingRect.contains(rect.topLeft()) and self.boundingRect.contains(rect.bottomRight())):
				self.currentRect.setRect(rect)

	def mouseReleaseEvent_(self, currentState, previousState):
		super().mouseReleaseEvent_(currentState, previousState)

		if(self.Mode == BoundingBoxEventHandler.Mode.CREATE):
			if(self.wasLeftButtonReleased(currentState, previousState)):
				self.Mode 			= BoundingBoxEventHandler.Mode.NONE
				self.currentRect 	= None
		if(self.Mode == BoundingBoxEventHandler.Mode.DRAG):
			if(self.wasMiddleButtonReleased(currentState, previousState)):
				self.Mode 			= BoundingBoxEventHandler.Mode.HOVER
