def get_reviews_html():
    return """
<ul>
<li class="review critic_review">
    <div class="review_wrap">
        <div class="review_content">
            <div class="review_section">
                <div class="review_product_scores">
                    <ul class="scores">
                        <li class="review_product_score brief_metascore">
                            <span class="metascore_w small release positive">84</span>
                            <span class="label">Metascore</span>
                        </li>
                        <li class="review_product_score brief_critscore">
                            <span class="metascore_w small release positive indiv">80</span>
                            <span class="label">
                                <span class="name_only">Critic Score</span>
                            </span>
                        </li>
                    </ul>
                </div>
                <div class="review_product">
                    <a href="/music/our-raw-heart/yob">Our Raw Heart</a>
                </div>
                <div class="review_body">
                    Our Raw Heart is a crushing and stirring doom metal affair, a cathartic album created after guitarist and vocalist Mike Scheidt suffered a severe episode of diverticulitis early last year. It shines with a rare beauty. The music ebbs and flows from ballad-like meditations reminiscent of Earth to the caustic sludge of Yob’s early records.
                </div>
            </div>
            <div class="review_section review_actions">
                <ul class="review_actions">
                    <li class="review_action publication_title">The Quietus</li>
                    <li class="review_action post_date">Posted Jun 20, 2018</li>
                    <li class="review_action full_review">
                        <a rel="popup:external" class="external" href="http://thequietus.com/articles/24811-yob-our-raw-heart-album-review">Read full review</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>
</ul>
"""


def get_review_without_full_review():
    return """
<ul>
<li class="review critic_review">
    <div class="review_wrap">
        <div class="review_content">
            <div class="review_section">
                <div class="review_product_scores">
                    <ul class="scores">
                        <li class="review_product_score brief_metascore">
                            <span class="metascore_w small release positive">84</span>
                            <span class="label">Metascore</span>
                        </li>
                        <li class="review_product_score brief_critscore">
                            <span class="metascore_w small release positive indiv">80</span>
                            <span class="label">
                                <span class="name_only">Critic Score</span>
                            </span>
                        </li>
                    </ul>
                </div>
                <div class="review_product">
                    <a href="/music/our-raw-heart/yob">Our Raw Heart</a>
                </div>
                <div class="review_body">
                    Our Raw Heart is a crushing and stirring doom metal affair, a cathartic album created after guitarist and vocalist Mike Scheidt suffered a severe episode of diverticulitis early last year. It shines with a rare beauty. The music ebbs and flows from ballad-like meditations reminiscent of Earth to the caustic sludge of Yob’s early records.
                </div>
            </div>
            <div class="review_section review_actions">
                <ul class="review_actions">
                    <li class="review_action publication_title">The Quietus</li>
                    <div class="review_action post_date">Posted Jun 20, 2018</div>
                </ul>
            </div>
        </div>
    </div>
</li>
</ul>
"""


def get_first_review_html():
    return """
<ul>
<li class="review critic_review first_review">
    <div class="review_wrap">
        <div class="review_content">
            <div class="review_section">
                <div class="review_product_scores">
                    <ul class="scores">
                        <li class="review_product_score brief_metascore">
                            <span class="metascore_w small release positive">86</span>
                            <span class="label">Metascore</span>    
                        </li>
                        <li class="review_product_score brief_critscore">
                            <span class="metascore_w small release positive indiv">80</span>
                                <span class="label">
                                <span class="name_only">Critic Score</span>
                            </span>
                        </li>
                    </ul>
                </div>
                <div class="review_product">
                    <a href="/music/daytona/pusha-t">DAYTONA</a>
                </div>
                <div class="review_body">
                    Any flaws feel minor, and they only lightly chip at this monolithic piece of work, where commonplace rap stories breathe in ways they haven’t before. The mystery is this record’s greatest strength, and it lives in every crevice, spicing up what could otherwise just be a collection of especially hard bars.
                </div>
            </div>
            <div class="review_section review_actions">
                <ul class="review_actions">
                    <li class="review_action publication_title">The Quietus</li>
                    <li class="review_action post_date">Posted Jun 21, 2018</li>
                    <li class="review_action full_review">
                        <a rel="popup:external" class="external" href="http://thequietus.com/articles/24834-pusha-t-daytona-album-review">Read full review</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</li>
</ul>
"""