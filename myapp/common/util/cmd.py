from __future__ import absolute_import

# from celery import shared_task, current_task
# from apps.common.util import kill_process
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import subprocess as sub
import os
import threading


class RunCmd(threading.Thread):

    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd, stdout=sub.PIPE, stderr=sub.STDOUT)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()  # use self.p.kill() if process needs a kill -9
            self.join()
            return None
        else:
            return self.p


##########################################################################
##########################################################################

# R methods

##########################################################################
##########################################################################

def run_r(username, title, code):

    directory = "submissions/r/%s" % username
    file_dir = "%s/%s" % (directory, title)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as exception:
            print "Exception creating dir: " + exception.strerror

    path = default_storage.save(file_dir, ContentFile(code))

    command = [
        'r',
        '-f',
        str('%s/%s' % (settings.MEDIA_ROOT, path))
    ]

    # run the process in a thread with max 15 seconds run time
    result = RunCmd(command, 15).Run().stdout.read()

    # result is none when timeout occurs
    if result is None:
        return "Request time out, please try again."

    if (result != ''):
        try:
            default_storage.delete(path)
        except:
            pass

        start_index = result.find("[1]")
        end_index = result.rfind("\n>")
        result = result[start_index:end_index]
        return result

    # current_task.request.hostname
    return result


##########################################################################
##########################################################################

# JAVA methods

##########################################################################
##########################################################################


def compile_file(username, title, code):
    directory = "submissions/%s" % username
    file_dir = "%s/%s.java" % (directory, title)
    class_dir = "%s/%s.class" % (directory, title)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as exception:
            print "Exception creating dir: " + exception.strerror

    path = default_storage.save(file_dir, ContentFile(code))

    command = [
        'javac',
        str('%s/%s' % (settings.MEDIA_ROOT, path))
    ]
    # result = sub.Popen(
    #    command, stdout=sub.PIPE, stderr=sub.STDOUT).stdout.read()

    result = kill_process.RunCmd(command, 60).Run().stdout.read()

    # result is none when timeout occurs
    if result is None:
        return "Request time out, please try again."

    if (result != ''):
        try:
            default_storage.delete(path)
            default_storage.delete(class_dir)
        except:
            pass

        start_index = result.find("error:")
        result = result[start_index:]
        return result

    # current_task.request.hostname
    return result


# @shared_task
def java_file(username, title, args, display_execution_time=False):
    execution_time = None
    if display_execution_time:
        command = [
            'time',
            '-p',
            'java',
            '-classpath',
            # str('%s/%s' % (settings.MEDIA_ROOT, path))
            str('%s/submissions/%s' % (settings.MEDIA_ROOT, username)),
            title
        ]
    else:
        command = [
            'java',
            '-classpath',
            # str('%s/%s' % (settings.MEDIA_ROOT, path))
            str('%s/submissions/%s' % (settings.MEDIA_ROOT, username)),
            title
        ]

    if args and len(args) > 0:
        command = command + args

    result = sub.Popen(
        command, stdout=sub.PIPE, stderr=sub.STDOUT).stdout.read()

    # Run the java command in another thread which will be killed after the
    # timeout
    result = kill_process.RunCmd(command, 60).Run().stdout.read()

    # result is none when timeout occurs
    if result is None:
        return "Time out", execution_time

    if display_execution_time:
        start_index = result.rfind('real')
        end_index = result.rfind('user')
        # 4 is length of real, 9 is the number of spaces
        # e.g. output ---- '<output values>        0.21 real         0.10 user         0.03 sys\n'
        execution_time = result[start_index + 4:end_index - 1].strip(' \t\n\r')
        #result_index = result[:start_index].rfind('        ')
        result = result[0:start_index - 1]

    return result, execution_time
