from django.shortcuts import render, redirect
from django.views import View
from todo_app.models import Task, Comment, Tag
from todo_app.forms import TaskForm, CommentForm, TagForm

class HomeView(View):
    def get(self, request):
        tasks = Task.objects.all()
        task_form = TaskForm()
        html_data =  {
            'task_list': tasks,
            'form': task_form
        }
        return render(
            request = request,
            template_name= 'index.html',
           
            context = html_data
        )
    def post(self, request):
        task_form = TaskForm(request.POST)
        task_form.save()
        return redirect('home')
class TaskDetailView(View):
    def get(self,request,task_id):
        task = Task.objects.get(id=task_id)
        task_form = TaskForm(instance=task)
        comment = Comment.objects.filter(task_id=task)
        comment_form = CommentForm(task_object=task)
        current_tags = task.tags.all()
        tag_form = TagForm()
        html_data = {
            'task': task,
            'form' : task_form,
            'tag_form': tag_form,
            'comment_list': comment,
            'comment_form': comment_form,
            'tag_list': current_tags
        }
        return render (
            request = request,
            template_name= 'detail.html',
            context = html_data
        )
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task_form = TaskForm(request.POST, instance=task)
        if 'update' in request.POST: 
            task_form.save()
        elif 'delete' in request.POST:
            task.delete()
        elif 'add' in request.POST:
            comment_form = CommentForm(request.POST, task_object= task)
            comment_form.save()
            return redirect('task_detail', task.id)
        elif 'tag' in request.POST:
            tag_form = TagForm(request.POST)
            tag_form.save(task)
            return redirect('task_detail', task.id)
        return redirect('home')