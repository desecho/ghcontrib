import json
import re

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ghcontrib.github import Github
from ghcontrib.models import Commit, Repo, User

from .mixins import AjaxView, TemplateAnonymousView, TemplateView


class HomeView(TemplateAnonymousView):
    template_name = 'home.html'

    def get_context_data(self):
        users = User.objects.exclude(username='admin')
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        return {'usernames': users.values_list('username', flat=True)}


class ContribsView(TemplateAnonymousView):
    template_name = 'contribs.html'

    def get_context_data(self, username):  # pylint: disable=no-self-use
        user = get_object_or_404(User, username=username)
        return {'repos': user.repos.all(), 'user': user}


class MyContribsView(TemplateView):
    template_name = ''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        return redirect(reverse('contribs', args=(self.request.user.username, )))


class MyReposView(TemplateView):
    template_name = 'my_repos.html'

    def get_context_data(self, **kwargs):
        repos = [{'id': repo.id, 'name': repo.name} for repo in self.request.user.repos.all()]
        kwargs['repos'] = json.dumps(repos)
        return kwargs


class RepoView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        name = self.request.POST['name']
        if re.match('.+/.+', name) is not None:
            user = self.request.user
            username, __ = name.split('/')
            if username == user.username:
                return self.fail(_('You cannot add your own repository'), self.MESSAGE_WARNING)
            if Github().repo_exists(name):
                if not user.repos.filter(name=name).exists():
                    repo_id = Repo.objects.create(name=name, user=user).pk
                    return self.success(id=repo_id)
                return self.fail(_('Repository already exists'), self.MESSAGE_WARNING)
            return self.fail(_('Repository not found'))
        return self.fail(_('Repository name is incorrect'))

    def delete(self, *args, **kwargs):  # pylint: disable=unused-argument
        try:
            repo_id = int(kwargs['id'])
        except (KeyError, ValueError):
            return self.render_bad_request_response()
        user = self.request.user
        repos = user.repos.filter(pk=repo_id)
        if repos.exists():
            repos.delete()
        else:
            return self.fail(_('Repository not found'))
        return self.success()


class LoadCommitDataView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        user = self.request.user
        repos = user.repos.all()
        gh = Github()
        for repo in repos:
            commit_data = gh.get_commit_data(user.username, repo.name)
            if commit_data is None:
                name = repo.name
                return self.fail(_(f'Repository {name} not found'))
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                Commit.objects.create(repo=repo, url=commit['url'], message=commit['message'], date=commit['date'])
        return self.success()
