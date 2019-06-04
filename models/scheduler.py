from gluon.scheduler import Scheduler
from gluon import current

from feedback import _scheduled_builder

if settings.academy_mode:
    scheduler = Scheduler(db, migrate='runestone_', heartbeat=1)
    current.scheduler = scheduler
