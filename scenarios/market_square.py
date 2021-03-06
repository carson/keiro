import random
from keiro.scenario import Scenario
from fast.vector2d import Vec2d
from keiro import obstacle
from pedestrians.randomwalker import RandomWalkingAvoider


class MarketSquare(Scenario):
    world_size = (640, 480)

    def init(self):
        self.agent.position = Vec2d(10, 10)
        self.agent.goal = Vec2d(*self.world.size) - self.agent.position
        self.agent.angle = (self.agent.goal - self.agent.position).angle()

        for j in xrange(2):
            for i in xrange(4):
                blob = obstacle.Rectangle(
                    (i + 1) * 50 + 100 * i,
                    (j + 1) * 100 + 120 * j - 50,
                    100,
                    120
                )
                self.world.add_obstacle(blob)


class CrowdedMarketSquare(Scenario):
    def init(self):
        if self.parameter is None:
            self.parameter = 0

        self.agent.position = Vec2d(10, 10)
        self.agent.goal = Vec2d(*self.world.size) - self.agent.position
        self.agent.angle = (self.agent.goal - self.agent.position).angle()

        rects = []
        for j in xrange(2):
            for i in xrange(4):
                r = obstacle.Rectangle((i + 1) * 50 + 100 * i, (j + 1) * 100 + 120 * j - 50, 100, 120)
                rects.append(r)
                self.world.add_obstacle(r)

        for i in xrange(self.parameter):
            good = False
            u = RandomWalkingAvoider()

            while not good:  # generate random positions for pedestrians that are not inside obstacles...
                init_position = Vec2d(random.randrange(u.radius + 1, self.world.size[0] - u.radius - 1),
                                      random.randrange(u.radius + 1, self.world.size[1] - u.radius - 1))
                good = init_position.distance_to(self.agent.position) > 20

                for r in rects:
                    if not good:
                        break
                    good = good and not r._rect.inflate(u.radius * 3, u.radius * 3).collidepoint(init_position)

            u.position = init_position
            self.world.add_unit(u)
