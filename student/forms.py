from django import forms

from student.models import Student
from student.models import JuniorHighSchool
from student.models import ElementarySchool
from student.models import HomeRoom

grade_values = [
    (0, '学年'),
    (7, '中３'),
    (6, '中２'),
    (5, '中１'),
    (4, '小６'),
    (3, '小５'),
    (2, '小４'),
    (1, '小３'),
]

GRADE_CHOICES = (
    ('', '学年'),
    ('中３', '中３'),
    ('中２', '中２'),
    ('中１', '中１'),
    ('小６', '小６'),
    ('小５', '小５'),
    ('小４', '小４'),
    ('小３', '小３'),
)

SCHOOL_CHOICES = (
    ('', '校舎'),
    ('本校', '本校'),
    ('橋戸校', '橋戸校'),
    ('瀬谷校', '瀬谷校'),
    ('大和校', '大和校'),
)


class StudentCreateForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"

    grade = forms.ChoiceField(
        widget=forms.Select,
        choices=GRADE_CHOICES,
    )

    school = forms.ChoiceField(
        widget=forms.Select,
        choices=SCHOOL_CHOICES,
    )

    birthday = forms.DateField(required=False)

    club = forms.CharField(required=False)

    parents = forms.CharField(required=False)

    siblings = forms.CharField(required=False)

    info = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class StudentUpdateForm(StudentCreateForm):

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        student = kwargs.get("instance")

        self.fields['home_room'] = forms.ChoiceField(
            required=False,
            widget=forms.Select,
            choices=(HomeRoom.objects.filter(grade=student.grade).values_list('name', 'name'))
        )

        # grade_values のリスト化
        grades = []
        # 生徒の学年番号の取得
        for grade in grade_values:
            if grade[1] == student.grade:
                grade_value = grade[0]
        for i in range(len(grade_values)):
            if grade_values[i][0] <= grade_value:
                # フォームに送るのは GRADE_CHOICES
                grades.append(GRADE_CHOICES[i])

        self.fields['entry_grade'] = forms.ChoiceField(
            required=False,
            widget=forms.Select,
            choices=(tuple(grades)),
        )

        # 学校名の選択を取得
        if '中' in student.grade:
            local_school_choices = (JuniorHighSchool.objects.values_list('name', 'name'))
        else:
            local_school_choices = (ElementarySchool.objects.values_list('name', 'name'))

        self.fields['local_school'] = forms.ChoiceField(
            required=False,
            widget=forms.Select,
            choices=local_school_choices,
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
