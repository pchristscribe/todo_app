from django.forms import ModelForm
from todo_app.models import Task, Comment, Tag

class TaskForm(ModelForm):
    class Meta():
        model = Task
        fields = ['description']
        labels = {
            'description': 'Task Description'
        }
class TagForm(ModelForm):
    '''When the user is trying to tag a Task object, use this form to 
        a) Create a new Tag with the given name if one does not exist, or
        b) Get the existing Tag with the given name if one does, then
        c) Connect the new or existing Tag to the given Task
    '''
    class Meta:
        model = Tag
        fields = ['name']
        labels = {'name' : 'Tag Name'}

    def save(self, task, *args, **kwargs):
        # `ModelForm`s come with an attribute called `self.data` that
        # keeps track of the data in the form as a dictionary.
        tag_name = self.data['name']

        # If a tag with this name already exists, we want to use that one,
        # not create a new tag with the same name (in fact this will error).
        # So let's `try` to get the existing tag, and if there isn't one,
        # create it from scratch

        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            # How did I know to catch the exception `Tag.DoesNotExist`?
            # I ran line 55 (trying to get a tag) on a nonexistant tag
            # to see what error it would create, then I caught that error
            tag = Tag.objects.create(name=tag_name)

        # Django has a built-in way to do the above try/except because it
        # is a process that happens so often:
        # tag, _ = Tag.objects.get_or_create(tag_name)

        # `get_or_create` returns 2 things:
        # 1) The object
        # 2) A boolean of whether or not it was created now or already existed
        # We can catch these two items separately, since we only want the object

        task.tags.add(tag) 
class CommentForm(ModelForm):
    # Pull the body column from the Comment model into a form
    class Meta():
        model= Comment
        fields = ['body']
        labels = {'body': ''}
    # the form will be created attached to a task_id/task_object_id    
    def __init__(self, *args, **kwargs):
        task = kwargs.pop('task_object')
        super().__init__(*args, **kwargs)
        #self.instance is the comment we are creating with this form
        self.instance.task = task
        self.fields['body'].label = ''


