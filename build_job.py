#!/usr/bin/env python3
import sys
import time
import urllib3

from src.apps.Jenkins.Infrastructure.ServerJenkinsRepository import ServerJenkinsRepository
from src.apps.Jenkins.Application.Build.JobBuilder import JobBuilder
from src.apps.Jenkins.Application.Find.BuildFinder import BuildFinder
from src.apps.Jenkins.Domain.JobParams import JobParams


def mandatory_arg(argv):
    if argv == "":
        raise ValueError("Required fields: jenkins url, jenkins api token, jenkins username and jenkins job")
    return argv


JENKINS_URL = mandatory_arg(sys.argv[1])
JENKINS_TOKEN = mandatory_arg(sys.argv[2])
JENKINS_USERNAME = mandatory_arg(sys.argv[3])
JENKINS_JOB_NAME = mandatory_arg(sys.argv[4])

# Optional args
JENKINS_JOB_PARAMS = sys.argv[5] if len(sys.argv) >= 5 else '{}'
JENKINS_WAIT_JOB = sys.argv[6] if len(sys.argv) >= 6 else "wait"
JENKINS_SSL_VERIFY = (sys.argv[7] == 'true') if len(sys.argv) >= 7 else true

if not JENKINS_SSL_VERIFY:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set Jenkins Connection
repository = ServerJenkinsRepository(url=JENKINS_URL, token=JENKINS_TOKEN, username=JENKINS_USERNAME, ssl_verify=JENKINS_SSL_VERIFY)

# Build Job
builder = JobBuilder(repository=repository)
builder.exec(name=JENKINS_JOB_NAME, params=JobParams(JENKINS_JOB_PARAMS))

# Get build number
finder = BuildFinder(repository=repository, name=JENKINS_JOB_NAME)
build_number = finder.number()
print(f"BUILD NUMBER: {build_number}")

if JENKINS_WAIT_JOB == "no-wait" and build_number:
    print("Job status is : EXECUTED")
    print("echo \"{job_status}=EXECUTED\" >> $GITHUB_OUTPUT")
    exit(0)

# Get build status
while not (status := finder.exec(build_number)):
    time.sleep(1)

print(f"Job status is : {status}")
print(f"echo \"{job_status}={status}\" >> $GITHUB_OUTPUT")
print(f"echo \"{job_build_number}={build_number}\" >> $GITHUB_OUTPUT")

if status != 'SUCCESS':
    exit(1)
