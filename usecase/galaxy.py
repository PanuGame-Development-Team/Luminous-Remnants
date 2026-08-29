from entity.entity import Entity
class Galaxy(Entity.Galaxy):
    def tick(self) -> None:
        for i in self.stars:
            i.tick()