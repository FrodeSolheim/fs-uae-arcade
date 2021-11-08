import functools


class Bezier(object):
    @classmethod
    @functools.lru_cache()
    def bezier_with_cache(cls, p0, p1, p2, p3, steps):
        return cls.bezier(p0, p1, p2, p3, steps)

    @classmethod
    def interpolate(cls, points, x):
        value = None
        # FIXME: Optimize
        for i, p in enumerate(points):
            if p[0] >= x:
                if i == 1:
                    value = p[1]
                    break
                else:
                    u = points[i - 1]
                    dx = p[0] - u[0]
                    dy = p[1] - u[1]
                    a = (x - u[0]) / dx
                    value = u[1] + dy * a
                    break
        if value is not None:
            return value
        # sometimes x (time) can be a bit more than max, due to
        # floating point rounding.. (weird that the less than check
        # in animation.py does not correct this..)
        return points[-1][1]

    @classmethod
    def bezier(cls, p0, p1, p2, p3, steps=20):
        x0, y0 = p0
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        ax = -x0 + 3 * x1 - 3 * x2 + x3
        ay = -y0 + 3 * y1 - 3 * y2 + y3
        bx = 3 * x0 - 6 * x1 + 3 * x2
        by = 3 * y0 - 6 * y1 + 3 * y2
        cx = -3 * x0 + 3 * x1
        cy = -3 * y0 + 3 * y1
        dx = x0
        dy = y0

        step_size = 1.0 / steps
        points = [(dx, dy)]
        for i in range(1, steps + 1):
            t = step_size * i
            x = ax * (t * t * t) + bx * (t * t) + cx * t + dx
            y = ay * (t * t * t) + by * (t * t) + cy * t + dy
            points.append((x, y))
        return points
