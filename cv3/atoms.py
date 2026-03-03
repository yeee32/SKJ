
import playground
import random as rn

from typing import List, Tuple, NewType

Pos = NewType('Pos', Tuple[int, int])


class Atom:

    def __init__(self, pos: Pos, vel: Pos, rad: int, col: str):
        """
        Initializer of Atom class

        :param x: x-coordinate
        :param y: y-coordinate
        :param rad: radius
        :param color: color of displayed circle
        """
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.rad = rad
        self.col = col


    def to_tuple(self) -> Tuple[int, int, int, str]:
        """
        Returns tuple representing an atom.

        Example: pos = (10, 12,), rad = 15, color = 'green' -> (10, 12, 15, 'green')
        """
        res = (self.pos_x, self.pos_y, self.rad, self.col)
        return res
        

    def apply_speed(self, size_x: int, size_y: int):
        """
        Applies velocity `vel` to atom's position `pos`.

        :param size_x: width of the world space
        :param size_y: height of the world space
        """
        if(self.pos_x + self.rad >= size_x):
            self.vel_x *= -1
        if(self.pos_y + self.rad >= size_y):
            self.vel_y *= -1
        if(self.pos_x - self.rad <= 0):
            self.vel_x *= -1
        if(self.pos_y - self.rad <= 0):
            self.vel_y *= -1

        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        


class FallDownAtom(Atom):
    """
    Class to represent atoms that are pulled by gravity.
     
    Set gravity factor to ~3.

    Each time an atom hits the 'ground' damp the velocity's y-coordinate by ~0.7.
    """
    def __init__(self, pos, vel, rad, col):
        super().__init__(pos, vel, rad, col)
        self.g = 3.0
        self.damping = 0.7

    def apply_speed(self, size_x, size_y):
        if(self.pos_x + self.rad >= size_x):
            self.pos_x = size_x - self.rad
            self.vel_x *= -1
        if(self.pos_y + self.rad >= size_y):
            self.pos_y = size_y - self.rad
            self.vel_y *= -self.damping
        if(self.pos_x - self.rad <= 0):
            self.pos_x = self.rad
            self.vel_x *= -1
        if(self.pos_y - self.rad <= 0):
            self.pos_y = self.rad
            self.vel_y *= -1

        self.vel_y += self.g

        self.pos_x += self.vel_x 
        self.pos_y += self.vel_y 


class ExampleWorld:

    def __init__(self, size_x: int, size_y: int, no_atoms: int, no_falldown_atoms: int):
        """
        ExampleWorld initializer.

        :param size_x: width of the world space
        :param size_y: height of the world space
        :param no_atoms: number of 'bouncing' atoms
        :param no_falldown_atoms: number of atoms that respect gravity
        """

        self.no_atoms = no_atoms
        self.no_falldown_atoms = no_falldown_atoms

        self.width = size_x
        self.height = size_y
        self.atoms = []

    def generate_atoms(self, no_atoms: int, no_falldown_atoms: int) -> List:
        """
        Generates `no_atoms` Atom instances using `random_atom` method.
        Returns list of such atom instances.

        :param no_atoms: number of Atom instances
        :param no_falldown_atoms: number of FallDownAtom instances
        """
        
        for i in range(no_atoms):
            self.atoms.append(self.random_atom())
        
        for i in range(no_falldown_atoms):
            self.atoms.append(self.random_falldown_atom())
        
        return self.atoms

    def random_atom(self) -> Atom:
        """
        Generates one Atom instance at random position in world, with random velocity, random radius
        and 'green' color.
        """
        rand_rad = rn.randint(7,15)
        rand_pos_x = rn.randint(rand_rad, self.width - rand_rad)
        rand_pos_y = rn.randint(rand_rad, self.height - rand_rad)
        rand_pos = (rand_pos_x, rand_pos_y)
        rand_vel = (rn.randint(-15,15), rn.randint(-15,15))
        rand_atom = Atom(rand_pos, rand_vel, rand_rad, "green")
        return rand_atom
        

    def random_falldown_atom(self):
        """
        Generates one FalldownAtom instance at random position in world, with random velocity, random radius
        and 'yellow' color.
        """
        rand_rad = rn.randint(6,20)
        rand_pos_x = rn.randint(rand_rad, self.width - rand_rad)
        rand_pos_y = rn.randint(rand_rad, self.height - rand_rad)
        rand_pos = (rand_pos_x, rand_pos_y)
        rand_vel = (rn.randint(1,6), rn.randint(1,6))
        rand_atom = FallDownAtom(rand_pos, rand_vel, rand_rad, "yellow")
        return rand_atom


    def add_atom(self, pos_x, pos_y):
        """
        Adds a new Atom instance to the list of atoms. The atom is placed at the point of left mouse click.
        Velocity and radius is random.

        :param pos_x: x-coordinate of a new Atom
        :param pos_y: y-coordinate of a new Atom

        Method is called by playground on left mouse click.
        """
        rand_rad = rn.randint(7, 15)
        rand_pos = (pos_x, pos_y)
        rand_vel = (rn.randint(-15, 15), rn.randint(-15, 15))
        new_atom = Atom(rand_pos, rand_vel, rand_rad, "green")
        self.atoms.append(new_atom)

    def add_falldown_atom(self, pos_x, pos_y):
        """
        Adds a new FallDownAtom instance to the list of atoms. The atom is placed at the point of right mouse click.
        Velocity and radius is random.

        Method is called by playground on right mouse click.

        :param pos_x: x-coordinate of a new FallDownAtom
        :param pos_y: y-coordinate of a new FallDownAtom
        """

        rand_rad = rn.randint(7, 15)
        rand_pos = (pos_x, pos_y)
        rand_vel = (rn.randint(-15, 15), rn.randint(-15, 15))
        new_atom = FallDownAtom(rand_pos, rand_vel, rand_rad, "yellow")
        self.atoms.append(new_atom)
        

    def tick(self):
        """
        Method is called by playground. Sends a tuple of atoms to rendering engine.

        :return: tuple or generator of atom objects, each containing (x, y, radius, color) attributes of atom 
        """

        res_atoms = []

        for atom in self.atoms:
            atom.apply_speed(self.width, self.height)
            res_atoms.append(atom.to_tuple())

        return tuple(res_atoms)

        #return ( (120, 60, 15, 'green',), (240, 300, 10, 'yellow',),)


if __name__ == '__main__':
    size_x, size_y = 700, 400
    no_atoms = 2
    no_falldown_atoms = 3

    world = ExampleWorld(size_x, size_y, no_atoms, no_falldown_atoms)
    world.generate_atoms(no_atoms, no_falldown_atoms)

    playground.run((size_x, size_y), world)
