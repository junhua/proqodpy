from django.db import modelsfrom django.utils.translation import ugettext_lazy as _from django.utils import timezonefrom django.contrib.postgres.fields import ArrayFieldclass CourseManager(models.Manager):    passclass Course(models.Model):    # Unique-together fields    course_batch = models.CharField(        _('course batch'),        max_length=20,        blank=True,        null=False,        help_text=_('e.g. FY15T3 (for Year 2015 Term 3)')    )    course_code = models.CharField(        _('course code'),        max_length=20,        blank=True,        null=False,        help_text=_('e.g. CS101')    )    school = models.CharField(        max_length=100,        blank=True,        null=True,        help_text=_('e.g. SUTD')    )    department = models.CharField(        max_length=100,        blank=True,        null=True,        help_text=_('e.g. ISTD')    )    # Other fields    title = models.CharField(        max_length=50,        blank=True,        null=True,        help_text=_('e.g. Digital World')    )    description = models.TextField(        max_length=255,        blank=True,        null=True,        help_text=_('e.g. An introduction course to programming using Python')    )    programming_language = models.CharField(        _('programming language'),        max_length=55,        blank=False,        null=False,        help_text=_('e.g. Python')    )  # e.g. Python    start_date = models.DateField(        _('start date'),        null=False,        blank=False    )    end_date = models.DateField(        _('end date'),        null=False,        blank=False    )    date_created = models.DateTimeField(        _('date created'),        default=timezone.now    )    # Foreign keys    participants = models.ManyToManyField(        'authnz.ProqodUser',        related_name='courses'    )    objects = CourseManager()    class Meta:        verbose_name = _('course')        verbose_name_plural = _('courses')        ordering = ['date_created']        unique_together = (            "course_batch", "course_code", "school", "department")    def get_absolute_path(self):        return "/courses/%i/" % self.pk    def __str__(self):        return "%s_%s_%s_%s" % (            self.school, self.department, self.course_code, self.title        )class Assessment(models.Model):    """    A short test of knowledge to particular topics that    can be a form of coding problem, MCQ or Blanks    """    LAB, QUIZ, PROJECT, EXAM = range(4)    ASSESSMENT_TYPE = (        (LAB, 'lab'),        (QUIZ, 'quiz'),        (PROJECT, 'project'),        (EXAM, 'exam'),    )    # fields    type = models.CharField(        _("type"),        max_length=5,        default=LAB,        choices=ASSESSMENT_TYPE,        null=False,        blank=False    )    label = models.CharField(        _("label"),        max_length=20,        null=False,        blank=False,    )    # If null, available all the time    start_datetime = models.DateTimeField(        _('start date time'),        null=True,        blank=True    )    end_datetime = models.DateTimeField(        _('end date time'),        null=True,        blank=True    )    # OneToMany: A course can have many quizes    course = models.ForeignKey('Course', related_name='quizes')    class Meta:        verbose_name = _('assessment')        verbose_name_plural = _('assessments')        ordering = ['type', 'label']        # unique_together = ("type", "label")    def __str__(self):        return "%s" % self.id        # return "course %s assessment %s type %s" % (        #     self.course.course_code, self.label, self.type        # )class Question(models.Model):    """    Question include 3 types (and others):    Programming, MCQ, Blanks.    """    PROGRAMMING, MCQ, BLANKS, OTHERS = range(4)    QUESTION_TYPE = (        (PROGRAMMING, "programming"),        (MCQ, "mcq"),        (BLANKS, "blank"),        (OTHERS, "others")    )    assessment = models.ForeignKey(        'Assessment',        null=True,        blank=True,        related_name="questions",    )    question_num = models.CharField(        _("question no"),        max_length=10,        null=False,        blank=False,        help_text="a question no unique together with the assessment"    )    type = models.CharField(        _("question type"),        max_length=5,        default=PROGRAMMING,        choices=QUESTION_TYPE    )    title = models.CharField(        _("title"),        max_length=50,        null=True,        blank=True    )    description = models.TextField(        _("description"),        null=True,        blank=True,    )    default_code = models.TextField(        _("default_code"),        null=True,        blank=True,    )    solution = models.TextField(        _("solution"),        null=True,        blank=True,    )    class Meta:        verbose_name = _('question')        verbose_name_plural = _('questions')        ordering = ['assessment', 'question_num']        unique_together = ("assessment", "question_num")    def __str__(self):        return "%s" % self.id        # return self.question_numclass MultipleChoice(models.Model):    """    Custom for Multiple Choice Questions.    """    content = models.CharField(        _("content"),        max_length=200,        null=False,        blank=True    )    question = models.ForeignKey(        "Question",        related_name="mcq_choices"    )    is_correct = models.BooleanField(        _("is correct"),        default=False    )    class Meta:        verbose_name = _('multiple_choice')        verbose_name_plural = _('multiple_choices')        ordering = ['question']        unique_together = ("question", 'content')    def __str__(self):        return "Question %s: %s" % (this.question.id, this.content)class BlankQuestionContent(models.Model):    """    Custom for Blank type of questions.    A blank is expected between each two parts.    seq is positive integer unique together with question.    """    part_seq = models.PositiveSmallIntegerField(        _("sequence"),        null=False,        blank=False,        help_text=_("sequence unique together with question")    )    content = models.CharField(        _("content"),        max_length=200,        null=False,        blank=True    )    question = models.ForeignKey(        "Question",        null=False,        blank=False,        related_name="blank_parts"    )    class Meta:        verbose_name = _('blank_question_part')        verbose_name_plural = _('blank_question_parts')        ordering = ['question', 'part_seq']        unique_together = (            'part_seq', 'question'        )    def __str__(self):        return "%s" % self.idclass TestCase(models.Model):    """    Test case for question's solution checking.    Each test case will have an array of inputs and an array of expected outputs.    For programming questions, the array of expected_output will likely be one entry.    ArrayField expects regular shape.    """    PUBLIC, PRIVATE = range(2)    VISIBILITY = (        (PUBLIC, 'Public'),        (PRIVATE, 'Private'),    )    MATCHING, NUMBER, KEYWORDS = range(3)    TYPES = (        (MATCHING, "matching"),        (NUMBER, "number"),        (KEYWORDS, "keywords"),    )    question = models.ForeignKey(        'Question',        related_name="test_cases",    )    visibility = models.IntegerField(        default=PUBLIC,        choices=VISIBILITY    )    type = models.IntegerField(        _("type"),        default=MATCHING,        choices=TYPES,        help_text=_("type of test cases")    )    test_content = models.TextField(        _("test_content"),        max_length=100000,        null=False,        blank=False,        default="",        help_text=("purpose of the test case")    )    inputs = ArrayField(        models.CharField(            _("input_values"),            max_length=255,            default="",            null=True,            blank=True        ),        blank=True,        null=True,    )    expected_outputs = ArrayField(        models.TextField(            max_length=255,            default=""        ),        blank=True,        null=True,    )    def __str__(self):        return "%s" % self.id    class Meta:        verbose_name = _('test_case')        verbose_name_plural = _('test_cases')        ordering = ['question', 'type']