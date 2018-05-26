__author__ = 'vincent'
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import redisdemo




def schedulerjob(job,trigger,desc):

         scheduler = BlockingScheduler()
         scheduler.add_job(job, trigger, desc)
         try:
            scheduler.start()
         except(KeyboardInterrupt, SystemExit):
            scheduler.shutdown()


def job_rentalamount():
        redisdemo.rentalamount()
        desc="day_of_week='mon-sun', hour=24, minute=00,end_date='2017-12-30'"
        schedulerjob(redisdemo.rentalamount(), 'cron',desc )
