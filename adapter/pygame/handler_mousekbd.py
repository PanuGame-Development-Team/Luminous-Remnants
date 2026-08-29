from usecase.usecase import UseCase
from adapter.pygame.events import KeyDown,KeyUp,MouseDown,MouseMove,Tick
from adapter.settings import HANDLER
class MouseKBD(UseCase.Handler):
    ldown = 0
    rdown = 0
    speed = 0
    def emit(self,event:UseCase.Event):
        if event.type == KeyDown.type:
            if event.msg == "l":
                self.ldown = True
            elif event.msg == "r":
                self.rdown = True
        elif event.type == KeyUp.type:
            if event.msg == "l":
                self.ldown = False
            elif event.msg == "r":
                self.rdown = False
        elif event.type == MouseDown.type:
            event.msg.x -= UseCase.var.scroffset
            self.controller.set_pos(event.msg)
            self.controller.click()
        elif event.type == MouseMove.type:
            event.msg.x -= UseCase.var.scroffset
            self.controller.set_pos(event.msg)
        elif event.type == Tick.type:
            if not self.controller.showing:
                self.speed -= int(self.rdown) * HANDLER.SPEED_CONTROL_FACTOR
                self.speed += int(self.ldown) * HANDLER.SPEED_CONTROL_FACTOR
            self.speed = round(self.speed * HANDLER.SPEED_CONTROL_FACTOR,5)
            UseCase.var.scroffset += self.speed
            self.controller.pos.x -= self.speed
            self.controller.set_pos(self.controller.get_pos())
            self.controller.tick()