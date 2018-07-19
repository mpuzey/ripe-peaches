import unittest

from mock import patch, MagicMock

from src.collector.web import aoty


def get_reviews_html():
    return """
<!DOCTYPE html>
<html>
    <head></head>
    <title>The Needle Drop Reviews  - Album of The Year</title>
    <div class="albumBlock">
        <a href="/artist/3466-ghost-bc/">
            <div class="artistTitle">Ghost</div>
        </a>
        <a href="/album/3466-ghost-bc-prequelle.php">
            <div class="albumTitle">Prequelle</div>
        </a>
        <div class="ratingRowContainer">
            <div class="ratingRow">
                <div class="ratingBlock">
                    <div class="rating">80</div>
                    <div class="ratingBar green">
                        <div class="green" style="width:80%;"></div>
                    </div>
                    </div>
                    <div class="ratingText">
                        <a class="gray" href="https://www.youtube.com/watch?v=-L2Xv5-EmUo">Full Review</a>;
                    </div>
                </div>
        </div>
    </div>
    <div class="albumBlock">
        <a href="/artist/2376-sleep/">
            <div class="artistTitle">Sleep</div>
        </a>
        <a href="/album/108460-sleep-the-sciences.php">
            <div class="albumTitle">The Sciences</div>
        </a>
        <div class="ratingRowContainer">
        <div class="ratingRow">
        <div class="ratingBlock">
                <div class="rating">80</div>
                    <div class="ratingBar green">
                        <div class="green" style="width:80%;"></div>
                </div>
                </div>
                <div class="ratingText">
                    <a class="gray" href="https://www.youtube.com/watch?v=d5jWckdWqpM">Full Review</a>;
                </div>
            </div>
        </div>
    </div>
</html>
"""


class TestAOTY(unittest.TestCase):
    @patch('src.collector.web.aoty.requests')
    def test__aoty__get_reviews__WillReturnListOfReviews__WhenAOTYRespondsWithPublicationScreenHTML(self, mock_requests):

        response = MagicMock()
        response.text = get_reviews_html()
        mock_requests.get.return_value = response
        expected_reviews = [
            {
                'artist': 'Ghost',
                'publication_name': '57-the-needle-drop',
                'release_name': 'Prequelle',
                'score': '80',
                'link': 'https://www.youtube.com/watch?v=-L2Xv5-EmUo'
            },
            {
                'artist': 'Sleep',
                'publication_name': '57-the-needle-drop',
                'release_name': 'The Sciences',
                'score': '80',
                'link': 'https://www.youtube.com/watch?v=d5jWckdWqpM'
            }
        ]

        actual_reviews = aoty.get_reviews('57-the-needle-drop')

        self.assertEqual(actual_reviews, expected_reviews)
