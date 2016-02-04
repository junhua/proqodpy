from django.db import modelsfrom django.utils.translation import ugettext_lazy as _from django.utils import timezonefrom django.contrib.postgres.fields import ArrayField# from rest_framework.response import Responsefrom RestrictedPython.Guards import safe_builtinsimport threadingimport sysimport StringIOimport timeitimport numpy as npfrom guppy import hpy# import astclass Course(models.Model):    # Unique-together fields    course_batch = models.CharField(        _('course batch'),        max_length=20,        blank=True,        null=False,        help_text=_('e.g. FY15T3 (for Year 2015 Term 3)')    )    course_code = models.CharField(        _('course code'),        max_length=20,        blank=True,        null=False,        help_text=_('e.g. CS101')    )    school = models.CharField(        max_length=100,        blank=True,        null=True,        help_text=_('e.g. SUTD')    )    department = models.CharField(        max_length=100,        blank=True,        null=True,        help_text=_('e.g. ISTD')    )    # Other fields    title = models.CharField(        max_length=50,        blank=True,        null=True,        help_text=_('e.g. Digital World')    )    description = models.TextField(        max_length=10000,        blank=True,        null=True,        help_text=_('e.g. An introduction course to programming using Python')    )    programming_language = models.CharField(        _('programming language'),        max_length=55,        blank=False,        null=False,        help_text=_('e.g. Python')    )  # e.g. Python    start_date = models.DateField(        _('start date'),        null=False,        blank=False    )    end_date = models.DateField(        _('end date'),        null=False,        blank=False    )    date_created = models.DateTimeField(        _('date created'),        default=timezone.now    )    # Foreign keys    # participants = models.ManyToManyField(    #     'authnz.ProqodUser',    #     related_name='courses'    # )    class Meta:        verbose_name = _('course')        verbose_name_plural = _('courses')        ordering = ['date_created']        unique_together = (            "course_batch", "course_code", "school", "department")    def get_absolute_path(self):        return "/courses/%i/" % self.pk    def __str__(self):        return "%s_%s_%s_%s" % (            self.school, self.department, self.course_code, self.title        )class CohortClass(models.Model):    label = models.CharField(        _("label"),        max_length=10,        null=False,        blank=False,    )    course = models.ForeignKey(        'Course',        null=False,        blank=False,        related_name="cohort_classes"    )    students = models.ManyToManyField(        'authnz.ProqodUser',        related_name="cohort_classes_students"    )    teachers = models.ManyToManyField(        'authnz.ProqodUser',        related_name="cohort_classes_teachers"    )    def __str__(self):        return self.label# class TeachingAssistant(get_user_model()):#     passclass Week(models.Model):    number = models.PositiveSmallIntegerField(        _("week_number"),        null=False,        blank=False,    )    instruction = models.TextField(        _("instruction"),        null=True,        blank=True    )    course = models.ForeignKey(        'Course',        related_name='Weeks',        on_delete=models.CASCADE,    )    def __str__(self):        return "%s" % self.number    class Meta:        unique_together = ('course', 'number')class Assessment(models.Model):    """    A short test of knowledge to particular topics that    can be a form of coding problem, MCQ or Blanks    """    LAB, QUIZ, PROJECT, EXAM, COHORT, HOMEWORK, OPTIONAL = range(7)    TYPE = (        (LAB, 'lab'),        (QUIZ, 'quiz'),        (PROJECT, 'project'),        (EXAM, 'exam'),        (COHORT, 'cohort session'),        (HOMEWORK, 'homework'),        (OPTIONAL, 'optional exercise'),    )    # fields    type = models.CharField(        _("type"),        max_length=5,        default=LAB,        choices=TYPE,        null=False,        blank=False    )    label = models.CharField(        _("label"),        max_length=20,        null=False,        blank=False,        default=1    )    # If null, available all the time    start_datetime = models.DateTimeField(        _('start date time'),        null=True,        blank=True    )    end_datetime = models.DateTimeField(        _('end date time'),        null=True,        blank=True    )    cohort_classes = models.ManyToManyField(        'CohortClass',        related_name="+",        # on_delete=models.DO_NOTHING,    )    week = models.ForeignKey(        'Week',        null=True,        on_delete=models.CASCADE,        related_name='assessments'    )    class Meta:        verbose_name = _('assessment')        verbose_name_plural = _('assessments')        ordering = ['type', 'week']        # unique_together = ("type", "label")    def __str__(self):        # return "%s" % self.id        return "course: %s assessment: %s type; %s" % (            self.course.course_code, self.label, self.type        )class Question(models.Model):    """    Question include 3 types (and others):    Programming, MCQ, Blanks.    """    PROGRAMMING, MCQ, BLANKS, CHECKOFF, OTHERS = range(5)    TYPE = (        (PROGRAMMING, "programming"),        (MCQ, "mcq"),        (BLANKS, "blank"),        (CHECKOFF, "check off"),        (OTHERS, "others")    )    assessment = models.ForeignKey(        'Assessment',        null=True,        blank=True,        on_delete=models.CASCADE,        # related_name="%(class)s",    )    number = models.PositiveSmallIntegerField(        _("number"),        null=False,        blank=False,        help_text="a question number unique together with the assessment"    )    type = models.PositiveSmallIntegerField(        _("question type"),        default=PROGRAMMING,        choices=TYPE    )    description = models.TextField(        _("description"),        null=True,        blank=True,    )    solution = models.TextField(        _("solution"),        null=True,        blank=True,    )    class Meta:        verbose_name = "%(class)s"        ordering = ['assessment', 'number']        unique_together = ("assessment", "number")        abstract = True    def __str__(self):        return "%s" % self.idclass ProgrammingQuestion(Question):    code_signature = models.CharField(        _("code_signature"),        max_length=50,        null=True,        blank=True    )    default_code = models.TextField(        _("default_code"),        null=True,        blank=True,        default="# YOUR CODE HERE"    )class BlankQuestion(Question):    passclass Mcq(Question):    passclass CheckoffQuestion(Question):    passclass MultipleChoice(models.Model):    """    Custom for Multiple Choice Questions.    """    content = models.CharField(        _("content"),        max_length=200,        null=False,        blank=True    )    question = models.ForeignKey(        "Mcq",        related_name="choices",        on_delete=models.CASCADE,    )    is_correct = models.BooleanField(        _("is correct"),        default=False    )    def __str__(self):        return self.content    class Meta:        verbose_name = _('multiple_choice')        verbose_name_plural = _('multiple_choices')        ordering = ['question']        unique_together = ("question", 'content')class BlankQuestionContent(models.Model):    """    Custom for Blank type of questions.    A blank is expected between each two parts.    seq is positive integer unique together with question.    """    part_seq = models.PositiveSmallIntegerField(        _("sequence"),        null=False,        blank=False,        help_text=_("sequence unique together with question")    )    content = models.CharField(        _("content"),        max_length=200,        null=False,        blank=True    )    question = models.ForeignKey(        "BlankQuestion",        null=False,        blank=False,        related_name="blank_parts",        on_delete=models.CASCADE,    )    class Meta:        verbose_name = _('blank_question_part')        verbose_name_plural = _('blank_question_parts')        ordering = ['question', 'part_seq']        unique_together = (            'part_seq', 'question'        )    def __str__(self):        return "%s" % self.idclass BlankSolution(models.Model):    """    Contains a solution set for a blank question    """    seq = models.PositiveSmallIntegerField(        _("sequence"),        null=False,        blank=False,        help_text=_("sequence unique together with question")    )    content = models.CharField(        _("content"),        max_length=200,        null=False,        blank=True    )    question = models.ForeignKey(        "BlankQuestion",        related_name="solution_set",        on_delete=models.CASCADE,    )    def __str__(self):        return "%s" % self.idclass TestCase(models.Model):    """    Test case for question's solution checking.    Each test case will have an array of inputs and an array of expected outputs.    For programming questions, the array of expected_output will likely be one entry.    ArrayField expects regular shape.    """    PRIVATE, PUBLIC = range(2)    VISIBILITY = (        (PUBLIC, 'Public'),        (PRIVATE, 'Private'),    )    MATCHING, NUMBER, KEYWORDS = range(3)    TYPES = (        (MATCHING, "matching"),        (NUMBER, "number"),        (KEYWORDS, "keywords"),    )    visibility = models.IntegerField(        default=PUBLIC,        choices=VISIBILITY    )    type = models.IntegerField(        _("type"),        default=MATCHING,        choices=TYPES,        help_text=_("type of test cases")    )    test_content = models.TextField(        _("test_content"),        max_length=10000,        null=True,        blank=True,        default="",        help_text=("purpose of the test case")    )    def __str__(self):        return "%s" % self.id    class Meta:        verbose_name = _('test_case')        verbose_name_plural = _('test_cases')        abstract = Trueclass UnitTest(TestCase):    question = models.ForeignKey(        'ProgrammingQuestion',        related_name="unittests",        on_delete=models.CASCADE,    )    inputs = ArrayField(        models.CharField(            _("input_values"),            max_length=255,            default="",            null=True,            blank=True        ),        blank=True,        null=True,        help_text=_("each input in its raw form")    )    expected_output = models.TextField(        _("expected_output"),        max_length=1024,        default="",        blank=True,        null=True,        help_text=_("expected output in string format")    )    def wrap_code(self, code):        # code = code.replace("\ndef", "\n@profile\ndef")        signature = self.question.code_signature        inputs = self.inputs        if len(inputs) == 0 or inputs[0] in ["[u'[]']", '[]']:            inputs = ""        else:            inputs = ",".join(["%s" % x for x in inputs])        last_line = "print '==output=='\nprint %s(%s)" % (signature, inputs)        output = "\n%s\n%s" % (code, last_line)        # raise Exception(output)        return output    def run(self, code, timeout=15):        """        run input code with wrapper. default timeout 15 sec        """        # https://pypi.python.org/pypi/RestrictedPython        # add import statement        # raise Exception(__builtins__.__import__)        sb = {'__import__': __import__}        sb.update(safe_builtins)        restricted_globals = dict(__builtins__=sb)        # raise Exception(restricted_globals)        codeOut = StringIO.StringIO()        codeErr = StringIO.StringIO()        sys.stdout = codeOut        sys.stderr = codeErr        output = self.expected_output        code = self.wrap_code(code)        def to_run():            exec code in restricted_globals        try:            t = threading.Thread(target=to_run)            t.start()            t.join(timeout)            if t.is_alive():                t.terminate()                t.join()                raise Exception(                    "Runtime exceed limits of %s seconds" % timeout)        except:            return {                "pass": False,                "error": "time out or fail to execute code."            }        sys.stdout = sys.__stdout__        sys.stderr = sys.__stderr__        result = codeOut.getvalue().strip() or codeErr.getvalue().strip()        if result:            result = result[                result.index("==output==") + len("==output==\n"):].strip()            return {                "pass": (result == output),                "output": result,                "time": self.time(code),                "memory": self.memory(code),            }        return {            "pass": False,            "error": codeErr.getvalue()        }    def time(self, code, times=3, number=10, complex=False, lang="Python"):        """        Measure the execution time for a snippet in microsecond.        times: number of runs to average the time estimate        number: number of iterations for each run        (TO BE IMPLEMENTED) If complex is set to True,         the function will return a line-by-line time report        """        try:            record = np.mean(timeit.repeat(code,                                           repeat=times,                                           number=number)) * 1000000 / number            return record        except:            return 0.    def memory(self, code):        """        Measure the memory for a snippet.        (TO BE IMPLEMENTED) If complex is set to True,         the function will return a line-by-line time report        """        restricted_globals = dict(__builtins__=safe_builtins)        memory_after, memory_before = range(2)        while(memory_after < memory_before):            try:                memory_before = hpy().heap().size                exec code in restricted_globals                memory_after = hpy().heap().size            except:                return 0.        return memory_after - memory_before