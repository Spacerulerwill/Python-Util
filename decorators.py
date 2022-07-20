# helpful decorators

import functools
from re import sub
import time
import warnings
import inspect
import math
from datetime import timedelta

def deprecated(reason=None):
  '''
  This is a decorator which can be used to mark functions
  as deprecated, giving a reason.
  '''
  if reason == None: reason = "No reason provided" 
  def decorator(func1):
    if inspect.isfunction(func1):
      msg = "Call to deprecated function: {name} - ({reason})"
    else:
      msg = "Call to deprecated class: {name} - ({reason})"
      
    @functools.wraps(func1)
    def new_func1(*args, **kwargs):
      warnings.simplefilter("always", DeprecationWarning)
      warnings.warn(
        msg.format(name=func1.__name__, reason=reason),
        category=DeprecationWarning,
        stacklevel=2,
      )
      warnings.simplefilter("default", DeprecationWarning)
      return func1(*args, **kwargs)
    return new_func1
  return decorator

def runtime():
  '''
  This is a decorator which can be used to find the runtime of a function
  '''
  def decorator(func1):
    @functools.wraps(func1)
    def new_func1(*args, **kwargs):
      startTime = time.monotonic()
      result =  func1(*args, **kwargs)
      endTime = time.monotonic()         
      print(f"Execution time: {timedelta(seconds=endTime-startTime)}")
      return result
    return new_func1
  return decorator
  
def check_progress_bar_variables(width, step, title, progress_char, other_char):
  '''
  Function that assess whether the input variables for progress bar are valid
  '''
  #default values
  if width == None: width = 20
  if step == None: step = 0.01
  if title == None: title == ""
  if progress_char == None: progress_char="█"
  if other_char == None: other_char = "-"

  #ensure all of correct types
  if not isinstance(width, int): raise TypeError("width must be an int")
  if not (isinstance(step, float) or isinstance(step, int)): raise TypeError("step must be a float")
  if not isinstance(progress_char, str): raise TypeError("progress_char must string of length 1")
  if not isinstance(other_char, str): raise TypeError("other_char must be a string of length 1")

  #parameter constraints
  if not 0.01 <= step <= 1: raise ValueError("step must be in range: 0.01 <= step <= 1")
  if len(progress_char) != 1: raise ValueError("progress_char must be a string of length 1")
  if len(other_char) != 1: raise ValueError("other_char must be a string of length 1")

  return width,step,title,progress_char,other_char

def progress_bar(width=None, step=None, title=None, progress_char=None, other_char=None):
  '''
  This is a decorator used to display a progress bar
  which updates when the function yeilds a value of
  progress between 0 and 1.
  '''
  width,step,title,progress_char,other_char= check_progress_bar_variables(width, step, title, progress_char, other_char)

  def decorator(func1):
    @functools.wraps(func1)
    def new_func1(*args, **kwargs):
      pb = ProgressBar(width, step, title, progress_char, other_char)
      progress_generator = func1(*args, **kwargs)
      if title != None:
        print(title)
      try:
        while True:
          progress = next(progress_generator)
          if isinstance(progress, int) or isinstance(progress, float): # if it's a number, treat it as a progress value 
            if progress - pb.progress > step:
              pb.set_progress(progress, end="\r")
          else:
            raise TypeError("Yielded value must be a int or float")
      except StopIteration as result:
        pb.set_progress(1.0)
        return result.value
    return new_func1
  return decorator

class ProgressBar():
  '''
  The class used for handling progress bars
  '''
  def __init__(self, width=None, step=None, title=None, progress_char=None, other_char=None):
    #default values
    self.width, self.step, self.title, self.progress_char, self.other_char = check_progress_bar_variables(width, step, title, progress_char, other_char)
    self.progress = 0
    
  def set_progress(self, progress, end=None):
    if end == None: end = "\n"
    if progress < 0 or progress > 1: raise ValueError("Yeilded progress must be between 0 and 1")
    self.progress = progress
    print(self, end=end)
    
  def __str__(self):
    progress = math.floor(self.progress * self.width)
    remaining = (self.width - progress)
    result =  self.progress_char * progress + self.other_char * remaining + " " + str(round(self.progress*100)) + "%" 
    return result


@progress_bar()
def iterateToNum(num):
  onePercent = 0.01 * num
  for i in range(num):
    if i % onePercent == 0:
      yield i / num

iterateToNum(10000000)