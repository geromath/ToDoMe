from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from root.highscorelist.forms import ScoreForm
from django.views import View
from django.response import Response
from root.highscorelist.models import leaderboard


def highscorelist(request, quiz, page=1):
    # display leaderboard table
    scores = leaderboard.leaders(int(page))
    if not scores:
        scores = []
    total_pages = int(leaderboard.total_pages())

    # Pagination values
    has_next = True if (page < total_pages) else False
    has_prev = True if (page != 1) else False
    next_page = page + 1 if has_next else page
    prev_page = page - 1 if has_prev else page

    # hashmap to get the score instance quickly
    score_list = {}

    # Collect the user ids
    user_ids = []
    for score in scores:
        user_ids.append(score["user"])
        score_list[int(score["user"])] = score

    # Fetch users in question
    users = User.objects.filter(pk__in=user_ids)

    for user in users:
        score_list[user.pk]["user"] = user

    return render_to_response("ToDoMe/highscorelist.html",
                              {
                                  "scores": scores,
                                  "total_pages": total_pages,
                                  "quiz": quiz,
                                  "page": page,
                                  'has_next': has_next,
                                  'has_prev': has_prev,
                                  'next_page': next_page,
                                  'prev_page': prev_page,
                              }, context_instance=RequestContext(request))


class ScoresView(View):
    # The manage scores on the leaderboard
    form = ScoreForm

    def get(self, page=1):
        #Returns the high scores
        scores = leaderboard.leaders(int(page))
        total_pages = leaderboard.total_pages()
        return {
            "participants":
                {
                    "total_pages": int(total_pages)
                },
            "scores": scores if scores else []
        }

    def post(self, request):
        """
        Creates new rankings
        Params:
            game: game identifier
            user_id: pk of the user
            score: positive integer
        Returns:
            1 on creation, 0 on update
        """

        user_id = request.POST.get('user_id')
        score = request.POST.get('score')

        try:
            user = User.objects.get(pk=user_id)
        except:
            return Response(404, 'User Not Found')

        status = leaderboard.rank_member(user.id, int(score))
        return {"status": status}

    def delete(self, request):
        pass


class ScoresAroundMeView(View):
    def get(self, user_id):
        #Returns the scores around the user
        scores = leaderboard.around_me(user_id)

        return {
            "participants": {leaderboard.around_me(user_id)},
            "scores": scores if scores else []
        }
