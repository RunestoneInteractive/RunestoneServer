from gluon.scheduler import Scheduler
from gluon import current

if settings.academy_mode:
    scheduler = Scheduler(db, migrate='runestone_')
    current.scheduler = scheduler