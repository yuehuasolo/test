from thunder_ase.fireball import Fireball
from ase.build import molecule
import timeit
from ase import units
# Socket Communication
from ase.calculators.socketio import SocketIOCalculator
# ase MD modules
from ase.md.verlet import VelocityVerlet as NVE


def run_with_socket():
    # Construct Structure
    atoms = molecule('C60')

    # set Fdata dir
    Fdata_path = 'Fdata'

    # Sockets
    unixsocket = 'thunder-ase'

    max_step = 10
    kwargs = {
              'ipi': 1,
              'nstepf':max_step+1,  # max step
              'inet': 0,
              'host': unixsocket,
              'scf_tolerance_set':1E-8,
              }
    fireball = Fireball(command='./fireball-ase.x', Fdata_path=Fdata_path, **kwargs)
    fireball.prefix = ''
    dyn = NVE(atoms, trajectory='md.traj', logfile='md.log', timestep=0.5 * units.fs)

    with SocketIOCalculator(fireball, log=None, unixsocket=unixsocket) as calc:
        atoms.calc = calc
        dyn.run(max_step)

print(timeit.timeit(run_with_socket, number=1))
