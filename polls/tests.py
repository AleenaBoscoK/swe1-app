import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(question_text, days=0):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        question = create_question("Recent?", days=0)
        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        question = create_question("Old?", days=-2)
        self.assertIs(question.was_published_recently(), False)

    def test_str_returns_question_text(self):
        question = create_question("What's up?")
        self.assertEqual(str(question), "What's up?")


class IndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_lists_questions(self):
        question = create_question("What's up?")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])


class DetailAndResultsViewTests(TestCase):
    def test_detail_shows_question_and_choices(self):
        question = create_question("Pick one")
        question.choice_set.create(choice_text="Option A")
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, "Pick one")
        self.assertContains(response, "Option A")

    def test_detail_missing_question_returns_404(self):
        response = self.client.get(reverse("polls:detail", args=(999,)))
        self.assertEqual(response.status_code, 404)

    def test_results_page(self):
        question = create_question("Pick one")
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertContains(response, "Pick one")


class VoteViewTests(TestCase):
    def test_vote_increments_and_redirects(self):
        question = create_question("Pick one")
        choice = question.choice_set.create(choice_text="Option A")
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": choice.id}
        )
        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_without_choice_shows_error(self):
        question = create_question("Pick one")
        response = self.client.post(reverse("polls:vote", args=(question.id,)), {})
        self.assertContains(response, "select a choice.")
