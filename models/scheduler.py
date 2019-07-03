from gluon.scheduler import Scheduler
from gluon import current

from feedback import _scheduled_builder

if settings.academy_mode:
    scheduler = Scheduler(db, migrate=table_migrate_prefix, heartbeat=1)
    current.scheduler = scheduler